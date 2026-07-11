# SmartRecipe AI — דף הכנה למצגת DevOps

> מסמך עזר למצגת. בנוי כרצף של "שקפים" עם נקודות דיבור. אפשר להעתיק כל סעיף כשקף בפני עצמו, או להשתמש במסמך כסקריפט להרצאה.

---

## 0. אג'נדה

1. מה זה הפרויקט ולמה הוא קיים
2. ארכיטקטורה — מה רץ על מה
3. איך בניתי את ה-Pipeline (CI/CD)
4. איך מתמודדים עם שגיאות — בכל שכבה
5. בדיקות אוטומטיות — GitHub Actions + pytest
6. ניטור ואבטחה
7. סיכום ולקחים

---

## 1. מה זה הפרויקט

**SmartRecipe AI** — אפליקציית ווב שמייצרת מתכונים בעזרת בינה מלאכותית.

- המשתמש מזין מרכיבים שיש לו בבית (עגבנייה, עוף, שום...)
- **Gemini AI** של Google מחזיר מתכון מלא: הוראות הכנה, זמן בישול, מידע תזונתי
- אפשר לשמור מתכונים ל-**MySQL**, לדרג, למחוק, ולקבל הצעות וריאציה מה-AI

**נקודת הדיבור המרכזית:** הפרויקט הוא לא רק "אפליקציה עם AI" — הוא הדגמה מלאה של מחזור **DevOps**: `Plan → Code → Build → Test → Release → Deploy → Operate → Monitor`, כשכל שלב ממומש בפועל ולא רק מוצהר.

---

## 2. ארכיטקטורה — מה רץ על מה

```
משתמש (דפדפן)
      │
      ▼
  Nginx :80        ← היחיד שחשוף לאינטרנט. שרת קבצים סטטיים + Reverse Proxy
      │
      ▼
  Flask :5000      ← Backend פנימי בלבד, לוגיקה עסקית + REST API
      │
      ├──▶  MySQL :3306     ← בסיס נתונים, גם הוא פנימי בלבד
      │
      └──▶  Gemini API      ← שירות AI חיצוני בענן

  Prometheus :9090  ← איסוף מדדים מ-Flask כל 15 שניות
  Grafana    :3000  ← דשבורד ויזואלי בזמן אמת
```

**5 קונטיינרים נפרדים**, מנוהלים יחד ע"י קובץ `docker-compose.yml` אחד.

**עיקרון אבטחה מרכזי:** רק Nginx חשוף לאינטרנט. Flask ו-MySQL נמצאים ברשת Docker פנימית (`smartrecipe-net`) ולא נגישים ישירות מבחוץ — גם אם תוקף פורץ ל-Nginx, הוא לא מקבל גישה ישירה ל-DB.

---

## 3. איך בניתי את ה-Pipeline (CI/CD)

### הטריגר

כל `git push` לענף `main` (או `pull_request` אליו) מפעיל אוטומטית את ה-Workflow שמוגדר ב-`.github/workflows/ci-cd.yml`.

### שלושה Jobs, כל אחד תלוי בקודם (`needs`)

```
git push → main
      │
      ▼
┌─────────────────────────────┐
│ Job 1: TEST                 │
│ • MySQL אמיתי כ-service      │
│ • pytest -v --cov            │
│ • כשל → מייל + עצירה         │
└──────────────┬───────────────┘
               │ עובר
┌──────────────▼───────────────┐
│ Job 2: BUILD & PUSH          │
│ • docker buildx               │
│ • push ל-Docker Hub           │
│   :latest + :sha-<hash>       │
│ • כשל → מייל + עצירה          │
└──────────────┬───────────────┘
               │
┌──────────────▼───────────────┐
│ Job 3: DEPLOY                │
│ • SCP קבצי compose לשרת       │
│ • SSH → הרצת deploy.sh        │
│ • מייל הצלחה / כשלון          │
└───────────────────────────────┘
```

### נקודות דיבור חשובות

- **`needs: test`** ו-`needs: build-and-push`** — כל Job רץ רק אם קודמו הצליח. אין אפשרות לפרוס קוד שלא עבר בדיקות.
- **Tag Strategy** — כל build מקבל שני תגיות: `:latest` (תמיד הגרסה העדכנית) ו-`:sha-<commit-hash>` (immutable, מאפשר **Rollback** מדויק לכל commit).
- **`if: github.ref == 'refs/heads/main'`** — Build ו-Deploy רצים רק ב-push ל-main, לא ב-Pull Request. כך PR מקבל רק בדיקות, לא deploy.
- **Cache** — `cache-from/cache-to: type=gha` מאיץ build חוזרים ע"י שמירת שכבות Docker בין ריצות.

### deploy.sh — מה קורה בפועל בשרת

```bash
docker compose pull                 # משיכת images חדשים מ-Docker Hub
docker compose run --rm backend flask db upgrade   # migration אם צריך
docker compose up -d --remove-orphans               # restart בלי downtime
docker image prune -f                                # ניקוי images ישנים
```

---

## 4. איך מתמודדים עם שגיאות — בכל שכבה

> זה הסעיף שממחיש **חשיבה DevOps אמיתית**: לא רק "לכתוב קוד שעובד", אלא לבנות מערכת שיודעת להיכשל בבטחה ולהתריע.

### 4.1 ברמת ה-Pipeline — עצירה אוטומטית + התראה במייל

בכל שלב קריטי (test / build / deploy) יש `if: failure()` שמפעיל שליחת מייל אוטומטית דרך `dawidd6/action-send-mail@v3`:

```yaml
- name: Send failure email
  if: failure()
  uses: dawidd6/action-send-mail@v3
  with:
    subject: "❌ CI FAILED — tests failed on commit ${{ github.sha }}"
    body: |
      Pipeline failed at: Test stage
      Commit: ${{ github.sha }}
      View: https://github.com/${{ github.repository }}/actions/runs/${{ github.run_id }}
```

**הרעיון:** אם בדיקה נכשלת — הפייפליין **נעצר מיד**. אין אפשרות ש-build פגום או קוד שבור יגיעו ל-Docker Hub או לשרת הייצור. גם בהצלחת ה-Deploy נשלח מייל אישור.

### 4.2 ברמת התלות בין שירותים — Healthcheck

בעיה קלאסית: Flask עולה לפני ש-MySQL מוכן לקבל חיבורים → קריסה.

```yaml
db:
  healthcheck:
    test: ["CMD", "mysqladmin", "ping", "-h", "localhost", "-u", "smartrecipe", ...]
    interval: 10s
    retries: 5

backend:
  depends_on:
    db:
      condition: service_healthy   # ← מחכה שה-DB יהיה healthy, לא רק "רץ"
```

### 4.3 ברמת קריאות ה-AI — Gemini עלול להיכשל

קריאה ל-API חיצוני יכולה להיכשל מכל סיבה: rate limit, timeout, בעיית רשת.

```python
try:
    recipe_data = generate_recipe(ingredients, preferences)
except Exception as e:
    return jsonify({"error": f"AI generation failed: {str(e)}"}), 500
```

- הודעת שגיאה ידידותית חוזרת ללקוח (`HTTP 500`)
- השגיאה נרשמת ב-logs של Gunicorn לתחקור
- **אין fallback** למתכון מוכן מראש — במכוון. זו אפליקציה שתלויה מטבעה ב-AI, ועדיף למשתמש לדעת שהיה כשל ולנסות שוב מאשר לקבל תוצאה מזויפת
- **חשוב:** שאר האפליקציה (שמירה/צפייה/מחיקה של מתכונים) **לא תלויה** ב-Gemini וממשיכה לעבוד רגיל גם אם ה-AI נופל

### 4.4 ברמת ה-Input — Validation לפני כתיבה ל-DB

```python
required = ["title", "ingredients", "instructions"]
for field in required:
    if field not in data:
        return jsonify({"error": f"'{field}' is required"}), 400
```

כל endpoint שכותב ל-DB בודק שדות חובה ומחזיר `400` ברור לפני שהוא נוגע במסד הנתונים.

### 4.5 ברמת ה-DB — הגנה מ-SQL Injection

שימוש ב-**SQLAlchemy ORM** במקום שאילתות SQL גולמיות:

```python
# בטוח — ORM מבצע escaping אוטומטי
Recipe.query.filter_by(title="Pasta").first()

# מסוכן — לעולם לא נכתב כך בפרויקט
cursor.execute(f"SELECT * FROM recipes WHERE title = '{user_input}'")
```

### 4.6 ברמת הסודות (Secrets) — מניעת חשיפה

- קובץ `.env` מקומי, מוגן ע"י `.gitignore` — אף פעם לא מגיע ל-Git
- `.env.example` הוא תבנית **ללא ערכים אמיתיים** — משמש רק כדוגמה למבנה
- בפייפליין: **GitHub Secrets** מוצפנים, לא נחשפים ב-logs
- בקוד: גישה אך ורק דרך `os.getenv()` — אף מפתח לא hard-coded

> **טיפ למצגת:** אפשר לספר כאן חוויה אישית — "בזמן ההרצה המקומית כמעט הכנסתי בטעות מפתח API אמיתי ל-`.env.example` (שכן עוקב ב-git) במקום ל-`.env` — תפסתי את זה לפני commit ותיקנתי". זה דוגמה חיה לחשיבות ההפרדה בין קובץ תבנית לקובץ סודות בפועל.

### 4.7 ברמת ה-Deploy — Rollback

כל commit מקבל image עם tag `sha-<hash>` קבוע. אם גרסה חדשה שבורה בייצור:

```bash
# שינוי ל-tag של commit קודם ו-push מחדש → הפייפליין פורס גרסה יציבה
export IMAGE_TAG=sha-<previous-commit>
docker compose up -d
```

---

## 5. בדיקות אוטומטיות — GitHub Actions + pytest

### האסטרטגיה: DB אמיתי, לא Mock

הבדיקות רצות מול **MySQL אמיתי** שמורם כ-service בתוך ה-Runner של GitHub Actions — לא מסד נתונים מדומה:

```yaml
services:
  mysql:
    image: mysql:8.0
    ports: ["3307:3306"]
    options: >-
      --health-cmd="mysqladmin ping -h localhost -u smartrecipe --password=smartrecipe"
      --health-interval=10s
      --health-retries=5
```

**למה זה חשוב:** mock יכול "לעבור" גם אם ה-query האמיתי שגוי מבחינת תחביר SQL או טיפוסי נתונים. חיבור ל-DB אמיתי תופס בעיות אמיתיות.

### שני קבצי בדיקות

**`test_db.py`** — הכנסה/הוצאה ישירות מה-DB:
| בדיקה | מה נבדק |
|---|---|
| `test_insert_recipe` | הכנסת רשומה + קבלת ID |
| `test_retrieve_recipe` | שמירה ושליפה לפי שדה |
| `test_update_recipe` | עדכון שדה |
| `test_delete_recipe` | מחיקה ווידוא היעלמות |
| `test_recipe_to_dict` | סריאליזציה ל-JSON |

**`test_api.py`** — כל ה-endpoints דרך ה-server בפועל:
| בדיקה | מה נבדק |
|---|---|
| `test_health_endpoint` | `GET /health` → 200 |
| `test_list_recipes_empty` | `GET /api/recipes` מחזיר מבנה JSON תקין |
| `test_save_recipe` | `POST` → 201 + ID |
| `test_get_recipe` | `GET /:id` מחזיר את הרשומה הנכונה |
| `test_update_recipe` | `PUT` מעדכן ומחזיר את הערך החדש |
| `test_delete_recipe` | `DELETE` → אחר כך `GET` מחזיר 404 |
| `test_save_recipe_missing_field` | חסר שדה חובה → 400 |
| `test_generate_recipe_missing_ingredients` | קריאה ל-AI בלי מרכיבים → 400 |

### איך זה רץ ב-CI

```yaml
- name: Run tests
  working-directory: backend
  env:
    TEST_DATABASE_URL: mysql+pymysql://smartrecipe:smartrecipe@127.0.0.1:3307/smartrecipe_test
    GEMINI_API_KEY: test_key_placeholder
  run: pytest --cov=app --cov-report=xml -v
```

- `--cov=app --cov-report=xml` — מדידת **code coverage**, מועלה ל-Codecov (`continue-on-error: true` — לא מפיל את הפייפליין אם ההעלאה עצמה נכשלת, רק הבדיקות עצמן קריטיות)
- `conftest.py` מגדיר fixture ברמת session שיוצר את כל הטבלאות פעם אחת ומנקה בסיום — מהיר יותר מיצירה מחדש בכל טסט

### הרצה מקומית לפני push

```bash
docker compose up -d db
docker compose exec -e TEST_DATABASE_URL=mysql+pymysql://smartrecipe:smartrecipe@db:3306/smartrecipe_test \
  backend pytest -v
```

**נקודת דיבור:** ריצה מקומית לפני push היא הרגל — תופסים כשלים לפני שהם מגיעים ל-CI ומעכבים את כל הצוות.

---

## 6. ניטור — Prometheus + Grafana

- Prometheus מתחבר ל-`/metrics` של Flask כל 15 שניות (דרך `prometheus-flask-exporter`)
- מודד: כמות בקשות, זמני תגובה (p95 latency), שיעור שגיאות 5xx
- Grafana טוען דשבורד מוכן מראש אוטומטית (**Provisioning** — קונפיגורציה כקוד, לא הגדרה ידנית בממשק)

**נקודת דיבור:** ניטור נבנה **מהיום הראשון**, לא נוסף בדיעבד. זה מאפשר לזהות בעיות בזמן אמת ברגע שהאפליקציה עולה לייצור — לא לחכות לתלונת משתמש.

---

## 7. סיכום ולקחים

### מה מומש בפועל

| דרישה | מימוש |
|---|---|
| Backend + REST API | Flask + Gunicorn |
| Nginx — Reverse Proxy | ניתוב `/api/*` ל-Flask + הגשת קבצים סטטיים |
| DB + הגנה מפני Injection | MySQL + SQLAlchemy ORM |
| Containerization מלא | 5 שירותים ב-Docker Compose |
| ניהול Secrets | `.env` + `.gitignore` + GitHub Secrets |
| בדיקות אוטומטיות מול DB אמיתי | 13 בדיקות pytest |
| CI על כל push | GitHub Actions |
| התראת כשלון | מייל אוטומטי בכל שלב |
| רישום images | Docker Hub, tag כפול (`latest` + `sha`) |
| פריסה בענן | Hetzner + SSH deploy |
| ניטור | Prometheus + Grafana |

### 3 הלקחים המרכזיים למצגת

1. **כשל צריך לעצור את התהליך, לא להסתתר** — כל שכבה (pipeline / healthcheck / try-except / validation) בנויה כך שכשל נתפס מוקדם ומדווח, במקום להתפשט הלאה.
2. **בדיקות אמיתיות > בדיקות נוחות** — DB אמיתי ב-CI, לא mock, כי מוקים מסתירים בעיות אמיתיות.
3. **סודות לעולם לא בקוד** — שלוש שכבות הפרדה (`.env` מקומי, `.env.example` כתבנית בלבד, GitHub Secrets לפייפליין) מונעות דליפה בטעות.

### כיוונים עתידיים (אם נשאלים "מה הלאה")

- HTTPS עם Let's Encrypt
- Rate Limiting על קריאות ל-Gemini
- Kubernetes אם המערכת תגדל למספר רב של שירותים
- גיבוי אוטומטי יומי (`mysqldump`) ל-MySQL
