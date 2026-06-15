# ספר הפרויקט הסופי
# SmartRecipe AI — מחולל מתכונים חכם
### פיתוח מערכת ווב מלאה עם DevOps, CI/CD, ו-AI

**שם הסטודנט:** dshrppury  
**תאריך:** יוני 2026  
**קורס:** DevOps Engineering — פרויקט סיום  

---

## תוכן עניינים

1. [רקע תיאורטי — DevOps ותפיסות ארכיטקטורה](#1-רקע-תיאורטי)
2. [מונוליט מול מיקרו-שירותים](#2-מונוליט-מול-מיקרו-שירותים)
3. [רקע על GitOps ו-CI/CD](#3-gitops-ו-cicd)
4. [תיאור הפרויקט ומטרותיו](#4-תיאור-הפרויקט)
5. [ארכיטקטורת המערכת](#5-ארכיטקטורת-המערכת)
6. [שכבת ה-Frontend — Nginx](#6-שכבת-ה-frontend--nginx)
7. [שכבת ה-Backend — Python Flask](#7-שכבת-ה-backend--python-flask)
8. [שכבת הנתונים — MySQL](#8-שכבת-הנתונים--mysql)
9. [אינטגרציית AI — Gemini](#9-אינטגרציית-ai--gemini)
10. [קונטיינריזציה — Docker ו-Docker Compose](#10-קונטיינריזציה)
11. [תשתית — Hetzner Server](#11-תשתית--hetzner)
12. [ה-CI/CD Pipeline — GitHub Actions](#12-pipeline-cicd)
13. [ניטור — Prometheus ו-Grafana](#13-ניטור)
14. [אבטחה וניהול סודות](#14-אבטחה)
15. [בדיקות — pytest](#15-בדיקות)
16. [סיכום ומסקנות](#16-סיכום)

---

## 1. רקע תיאורטי

### מהו DevOps?

DevOps הוא גישה תרבותית וטכנולוגית שמטרתה לגשר בין צוותי פיתוח (Development) לצוותי תפעול (Operations). המטרה המרכזית היא לאפשר פריסת תוכנה מהירה, אמינה, ובטוחה יותר על ידי אוטומציה, שיתוף פעולה, ומשוב מתמיד.

עקרונות הליבה של DevOps:

| עיקרון | הסבר |
|---|---|
| **אוטומציה** | כל שלב חוזר — בנייה, בדיקות, פריסה — יש לאטמט |
| **אינטגרציה מתמשכת (CI)** | מפתחים ממזגים קוד לענף ראשי לעיתים קרובות |
| **פריסה מתמשכת (CD)** | כל שינוי שעובר בדיקות נפרס אוטומטית לסביבת ייצור |
| **ניטור ומשוב** | מדדים ולוגים מאפשרים זיהוי בעיות בזמן אמת |
| **תשתית כקוד (IaC)** | תשתיות מוגדרות בקבצי טקסט, מנוהלות ב-Git |

### מחזור חיי DevOps

```
Plan → Code → Build → Test → Release → Deploy → Operate → Monitor
  └──────────────────────────────────────────────────────────┘
                       (לולאה מתמשכת)
```

---

## 2. מונוליט מול מיקרו-שירותים

### ארכיטקטורת מונוליט

**מונוליט** הוא מערכת תוכנה שבה כל הרכיבים — ממשק משתמש, לוגיקת עסקים, וגישה לנתונים — מרוכזים ביישום אחד, שנפרס כיחידה אחת.

**יתרונות:**
- פשוט לפיתוח ראשוני ולהבנה
- קל לדיבאג (הכל במקום אחד)
- ביצועים טובים בגלל העדר תקשורת רשת בין רכיבים
- פשוט לבדיקות end-to-end

**חסרונות:**
- כאשר המערכת גדלה, קשה לפתח ולתחזק
- סקיילינג של חלק ספציפי מחייב סקיילינג של כל המערכת
- עדכון חלק אחד מצריך פריסה מחדש של הכל
- הצמדות טכנולוגית (Tech Lock-in)

### ארכיטקטורת מיקרו-שירותים

**מיקרו-שירותים** הם גישה שמחלקת את היישום לשירותים קטנים ועצמאיים, כל אחד אחראי לדומיין עסקי מוגדר, מתקשר עם האחרים דרך API (בדרך כלל HTTP/REST או Message Queue).

**יתרונות:**
- כל שירות ניתן לפיתוח, פריסה, וסקיילינג באופן עצמאי
- צוותים שונים יכולים לעבוד על שירותים שונים במקביל
- גמישות טכנולוגית (שירות אחד יכול להיות ב-Python, אחר ב-Go)
- כשל מבודד — שירות שנופל לא מוריד את כל המערכת

**חסרונות:**
- מורכבות תפעולית גבוהה יותר
- תקשורת רשת בין שירותים מוסיפה latency
- קשיי consistency בנתונים מבוזרים
- צורך בכלי Orchestration (Kubernetes)

### הפרויקט הנוכחי — גישה היברידית

הפרויקט SmartRecipe AI מבוסס על **ארכיטקטורת שכבות** (Layered Architecture) בתוך מבנה קונטיינרים, המשלבת את יתרונות שתי הגישות:

- שירותים נפרדים (Nginx, Flask, MySQL, Prometheus, Grafana) ← מיקרו-שירותים
- לוגיקת האפליקציה בתוך Flask היא מונוליטית ← פשטות פיתוח
- Docker Compose מנהל את כל הסביבה ← תפעול פשוט

---

## 3. GitOps ו-CI/CD

### מהו GitOps?

**GitOps** הוא מודל תפעולי שמטפל ב-Git כמקור אמת יחיד (Single Source of Truth) לתשתיות ולקוד. כל שינוי — בין אם בקוד, בהגדרות, או בתשתית — עובר דרך Pull Request ב-Git.

עקרונות GitOps:
1. **הכל ב-Git** — קוד, Dockerfiles, docker-compose, scripts
2. **שינויים רק דרך PR** — לא עדכונים ידניים בשרת
3. **אוטומציה** — merge לענף ראשי מפעיל Pipeline
4. **ניטור ואמינות** — המערכת שואפת תמיד למצב המוגדר ב-Git

### מהי CI/CD?

**CI (Continuous Integration):** כל push לענף ראשי מפעיל אוטומטית:
- בדיקות אוטומטיות
- בנייה של Docker Images
- בדיקות איכות קוד

**CD (Continuous Deployment):** לאחר CI מוצלח, הקוד:
- נארז ל-Docker Images
- מועלה ל-Docker Registry
- נפרס אוטומטית לשרת הייצור

### מודל ה-CI/CD בפרויקט זה

```
Developer pushes code to GitHub (main branch)
                │
                ▼
      GitHub Actions triggered
                │
     ┌──────────▼──────────┐
     │   Job 1: TEST        │
     │  • Spin MySQL svc    │
     │  • pip install       │
     │  • pytest -v         │
     └──────────┬───────────┘
                │ pass
     ┌──────────▼──────────┐
     │  Job 2: BUILD-PUSH   │
     │  • docker buildx     │
     │  • push :latest +    │
     │    :sha-<hash>       │
     │  → Docker Hub        │
     └──────────┬───────────┘
                │
     ┌──────────▼──────────┐
     │  Job 3: DEPLOY       │
     │  • SCP compose files │
     │  • SSH → Hetzner     │
     │  • docker pull       │
     │  • docker compose up │
     └─────────────────────┘
```

---

## 4. תיאור הפרויקט

### SmartRecipe AI — מחולל מתכונים חכם

#### רקע ומוטיבציה

אחת הבעיות הנפוצות בחיי היומיום היא לעמוד מול מקרר מלא מרכיבים ולא לדעת מה לבשל. SmartRecipe AI פותרת בעיה זו: המשתמש מזין את המרכיבים הקיימים אצלו, ו-AI מודרני (Gemini 1.5 Flash של Google) מייצר מתכון מפורט ומותאם אישית.

#### מטרות הפרויקט

1. **מטרה טכנית:** הדגמת שליטה מלאה ב-stack DevOps מודרני
2. **מטרה פונקציונלית:** יצירת כלי שימושי אמיתי לניהול מתכונים עם AI
3. **מטרה לימודית:** הטמעת CI/CD, קונטיינריזציה, ניטור, ותשתית כקוד

#### פיצ'רים עיקריים

| פיצ'ר | תיאור |
|---|---|
| **יצירת מתכון** | הזנת מרכיבים → Gemini מייצר מתכון מלא עם הוראות, זמן הכנה, ומידע תזונתי |
| **שמירת מתכונים** | שמירה ב-MySQL, עם דירוג ומיון |
| **ניהול מתכונים** | צפייה, עדכון, מחיקה |
| **וריאציות AI** | קבלת 3 הצעות שינוי/החלפה ממרכיבים מ-Gemini |
| **פילטר לפי מטבח** | סינון המתכונים השמורים לפי סוג מטבח |
| **ניטור** | מדדי ביצועים בזמן אמת ב-Grafana |

---

## 5. ארכיטקטורת המערכת

### דיאגרם ארכיטקטורה

```
┌─────────────────────────────────────────────────────────────────┐
│                         HETZNER VPS                              │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐    │
│  │                   Docker Network (bridge)                 │    │
│  │                                                           │    │
│  │  ┌─────────────┐     ┌──────────────────┐               │    │
│  │  │    Nginx     │────▶│  Flask Backend   │               │    │
│  │  │  :80 (pub)  │     │  :5000 (intern)  │               │    │
│  │  └─────────────┘     └────────┬─────────┘               │    │
│  │                               │                           │    │
│  │                    ┌──────────▼──────────┐               │    │
│  │                    │   MySQL :3306        │               │    │
│  │                    │   (internal only)    │               │    │
│  │                    └─────────────────────┘               │    │
│  │                                                           │    │
│  │  ┌───────────────┐   ┌─────────────────────┐            │    │
│  │  │  Prometheus   │──▶│      Grafana         │            │    │
│  │  │  :9090 (pub)  │   │  :3000 (pub)         │            │    │
│  │  └───────────────┘   └─────────────────────┘            │    │
│  └──────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
              │                         │
              ▼                         ▼
       GitHub Actions            Google Gemini API
    (CI/CD Pipeline)              (חיצוני/ענן)
```

### תרשים רכיבים

```
GitHub Repository
├── .github/workflows/ci-cd.yml    ← Pipeline הגדרות
├── backend/                       ← Flask service
├── frontend/                      ← Nginx + HTML
├── monitoring/                    ← Prometheus + Grafana
├── infrastructure/                ← Hetzner scripts
├── docker-compose.yml             ← Dev environment
└── docker-compose.prod.yml        ← Production overrides
```

---

## 6. שכבת ה-Frontend — Nginx

### תפקיד Nginx בפרויקט

Nginx ממלא שני תפקידים מרכזיים:

1. **File Server סטטי** — מגיש את ה-HTML, CSS, ו-JavaScript של ממשק המשתמש
2. **Reverse Proxy** — מנתב בקשות API (`/api/*`) לשרת Flask הפנימי

### קובץ nginx.conf — ניתוח

```nginx
upstream backend {
    server backend:5000;
}
```
הגדרת upstream מאפשרת Load Balancing עתידי — ניתן להוסיף מספר instances של backend.

```nginx
location / {
    try_files $uri $uri/ /index.html;
}
```
תמיכה ב-SPA (Single Page Application) — כל route מנותב ל-index.html.

```nginx
location /api/ {
    proxy_pass http://backend;
    proxy_read_timeout 120s;
}
```
Timeout של 120 שניות עבור בקשות AI שעלולות לקחת זמן.

### יתרונות השימוש ב-Nginx

- **ביצועים:** Nginx הוא event-driven ומסוגל לנהל אלפי חיבורים במקביל
- **אבטחה:** הסתרת Flask מהרשת הציבורית
- **Security Headers:** הגנה מפני XSS ו-Clickjacking
- **Gzip:** דחיסת תגובות להפחתת bandwidth

### ממשק המשתמש — SPA

הממשק נבנה כ-Vanilla JavaScript SPA עם:
- **Tag Input** — הוספת מרכיבים כתגיות עם Enter
- **AI Generation Panel** — הצגת המתכון שנוצר
- **Recipe List** — רשימה ממוספרת עם pagination
- **Modal** — פרטי מתכון מלאים ב-overlay

---

## 7. שכבת ה-Backend — Python Flask

### מבנה האפליקציה — App Factory Pattern

```python
def create_app(config=None):
    app = Flask(__name__)
    db.init_app(app)
    migrate.init_app(app, db)
    metrics.init_app(app)
    CORS(app)
    app.register_blueprint(recipes_bp, url_prefix="/api")
    app.register_blueprint(health_bp)
    return app
```

**App Factory Pattern** מאפשר יצירת instances שונים של האפליקציה (dev, test, prod) עם קונפיגורציה שונה — חיוני לבדיקות.

### Blueprints — ניתוב

| Blueprint | קידומת | תיאור |
|---|---|---|
| `health` | `/` | Health check, endpoint ראשי |
| `recipes` | `/api` | כל פעולות ה-CRUD ו-AI |

### SQLAlchemy ORM

```python
class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    ingredients = db.Column(db.Text, nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    nutritional_info = db.Column(db.Text, nullable=True)
    cuisine_type = db.Column(db.String(100))
    prep_time_minutes = db.Column(db.Integer)
    rating = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
```

שימוש ב-ORM מספק:
- הגנה מובנית מ-SQL Injection
- Migrations אוטומטיות עם Flask-Migrate
- קוד Pythonic וקריא

### Flask-Migrate — ניהול Migrations

```bash
flask db init      # יצירת תיקיית migrations (פעם אחת)
flask db migrate   # יצירת migration חדשה
flask db upgrade   # החלת השינויים על ה-DB
```

זה מאפשר שינויים בסכמת הנתונים ללא מחיקת הנתונים הקיימים.

### Gunicorn — Production WSGI Server

```
gunicorn --bind 0.0.0.0:5000 --workers 4 --timeout 120 wsgi:app
```

- **4 workers** — מקביליות לעיבוד בקשות
- **timeout 120s** — מספיק לבקשות AI ארוכות
- Flask dev server לא מתאים לייצור (single-threaded, no process management)

---

## 8. שכבת הנתונים — MySQL

### מבנה הטבלה

```sql
CREATE TABLE recipes (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    title           VARCHAR(255) NOT NULL,
    ingredients     TEXT NOT NULL,
    instructions    TEXT NOT NULL,
    nutritional_info TEXT,
    cuisine_type    VARCHAR(100),
    prep_time_minutes INT,
    rating          FLOAT DEFAULT 0.0,
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### Healthcheck — מדוע חשוב?

```yaml
healthcheck:
  test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
  interval: 10s
  retries: 5
```

Flask תלוי ב-MySQL. ללא healthcheck, Flask עשוי לנסות להתחבר לפני שה-DB מוכן ולקרוס. `depends_on: condition: service_healthy` מבטיח סדר הפעלה נכון.

### Persistent Volume

```yaml
volumes:
  - db_data:/var/lib/mysql
```

הנתונים נשמרים גם לאחר `docker compose down`. בייצור, Volume ממופה לספרייה קבועה בשרת.

### בסיס נתונים לבדיקות

נוצר בסיס נתונים נפרד `smartrecipe_test` (ראה `mysql-init.sql`) שמשמש אך ורק לבדיקות — הנתונים הנמחקים בבדיקות לא פוגעים בנתוני הייצור.

---

## 9. אינטגרציית AI — Gemini

### Google Gemini API

Gemini הוא מודל שפה גדול (LLM) של Google. בפרויקט נעשה שימוש ב-**gemini-1.5-flash** — גרסה מהירה ויעילה מבחינת עלות.

### Prompt Engineering

```python
prompt = f"""You are a professional chef and nutritionist. 
Generate a detailed recipe using primarily these ingredients: {ingredients_str}.
{pref_text}

Respond ONLY with a valid JSON object (no markdown) in this exact structure:
{{
  "title": "Recipe Name",
  "ingredients": "...",
  "instructions": "...",
  "nutritional_info": "...",
  "cuisine_type": "...",
  "prep_time_minutes": 30
}}"""
```

**עקרונות ה-Prompt:**
1. **תפקיד ברור** — "Professional chef and nutritionist"
2. **פורמט מוגדר** — JSON בלבד, ללא markdown
3. **מבנה מוגדר** — מניעת תגובות לא עקביות
4. **Fallback** — ניקוי markdown אם Gemini מוסיף backticks

### אבטחת ה-API Key

המפתח מועבר אך ורק כ-Environment Variable:
```yaml
# docker-compose.yml
environment:
  GEMINI_API_KEY: ${GEMINI_API_KEY}
```

**לעולם לא** ב-קוד המקור או ב-Git!

### טיפול בשגיאות AI

```python
try:
    recipe_data = generate_recipe(ingredients, preferences)
except Exception as e:
    return jsonify({"error": f"AI generation failed: {str(e)}"}), 500
```

שגיאות API (rate limit, network) מוחזרות ל-client ב-HTTP 500 עם הסבר.

---

## 10. קונטיינריזציה

### Docker — עקרונות בסיסיים

**קונטיינר** הוא יחידת תוכנה בודדת הכוללת את הקוד, ה-runtime, הספריות, וקובצי הקונפיגורציה. הקונטיינר רץ באיזוריזציה מ-OS אך חולק את הקרנל.

**יתרונות:**
- **Reproducibility** — אותה סביבה בפיתוח, בדיקות, וייצור
- **Isolation** — כל שירות בסביבה נפרדת
- **Portability** — "Build once, run anywhere"

### Dockerfile — Backend

```dockerfile
FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev gcc pkg-config

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "wsgi:app"]
```

**best practices:**
- `python:3.12-slim` — image קטן (לא full)
- `--no-cache-dir` — הפחתת גודל image
- COPY `requirements.txt` לפני COPY קוד — שימוש ב-Docker layer cache

### Docker Compose — Multi-Service Orchestration

```yaml
services:
  db:          # MySQL
  backend:     # Flask
  frontend:    # Nginx
  prometheus:  # Metrics collection
  grafana:     # Metrics visualization
```

**Networks:** כל השירותים על רשת `smartrecipe-net` — Flask מדבר עם MySQL ב-`db:3306`, Nginx מדבר עם Flask ב-`backend:5000`.

**Health Checks:** MySQL חייב להיות ready לפני ש-Flask עולה.

### docker-compose.prod.yml — Production Override

בסביבת ייצור, תמונות Docker נמשכות מ-Docker Hub (לא בנויות locally):

```yaml
services:
  backend:
    image: ${DOCKER_HUB_USERNAME}/smartrecipe-backend:${IMAGE_TAG:-latest}
    build: ~    # מבטל את ה-build
```

---

## 11. תשתית — Hetzner

### למה Hetzner?

Hetzner Cloud הוא ספק ענן אירופי המציע VPS במחירים נמוכים יחסית. לפרויקט זה, VPS פשוט מספיק לעומת הפתרונות המנוהלים של AWS/GCP.

### תסריט ה-Provisioning

`hetzner_setup.sh` מכין שרת Ubuntu 22.04 חדש:

1. **עדכון packages** — `apt-get update && upgrade`
2. **התקנת Docker** — מה-repository הרשמי של Docker
3. **התקנת Docker Compose** — הורדת binary ישירות
4. **יצירת משתמש deploy** — `deploy` user עם הרשאות Docker
5. **קונפיגורציית UFW** — פתיחת פורטים 80, 443, 3000, 9090
6. **יצירת ספריות** — `/opt/smartrecipe/` עם תת-ספריות לנתונים

### deploy.sh — Zero-Downtime Deployment

```bash
docker compose pull          # משיכת images חדשים
flask db upgrade             # migration של DB
docker compose up -d         # restart שירותים
docker image prune -f        # ניקוי images ישנים
```

`docker compose up -d` עם images חדשים מחליף קונטיינרים רצים אחד-אחד, מה שמאפשר zero-downtime בתנאים מסוימים.

---

## 12. Pipeline CI/CD

### GitHub Actions — מבנה הפייפלין

הפייפלין מוגדר ב-`.github/workflows/ci-cd.yml` ומורכב מ-3 Jobs:

#### Job 1: test

```yaml
services:
  mysql:
    image: mysql:8.0
    ports: ["3307:3306"]
```

GitHub Actions מפעיל container של MySQL כ-service בתוך ה-runner. הבדיקות מתחברות ל-`127.0.0.1:3307` — **MySQL אמיתי**, לא mock.

```yaml
- name: Run tests
  env:
    TEST_DATABASE_URL: mysql+pymysql://...@127.0.0.1:3307/smartrecipe_test
  run: pytest --cov=app --cov-report=xml -v
```

#### Job 2: build-and-push

```yaml
- uses: docker/build-push-action@v5
  with:
    context: ./backend
    push: true
    tags: |
      dshrppury/smartrecipe-backend:latest
      dshrppury/smartrecipe-backend:sha-${{ github.sha }}
    cache-from: type=gha
    cache-to: type=gha,mode=max
```

**Tag strategy:**
- `:latest` — תמיד מצביע על הגרסה האחרונה
- `:sha-<hash>` — tag קבוע לכל commit, מאפשר rollback

**Docker layer cache:** שמירת cache ב-GitHub Actions cache → בניה מהירה יותר בפייפלינים הבאים.

#### Job 3: deploy

```yaml
- uses: appleboy/ssh-action@v1.0.3
  with:
    script: bash /opt/smartrecipe/infrastructure/deploy.sh
```

GitHub Actions מתחבר לשרת Hetzner ב-SSH ומריץ את `deploy.sh`.

### ניהול סודות ב-GitHub Secrets

| Secret | שימוש |
|---|---|
| `DOCKER_HUB_USERNAME` | שם משתמש ב-Docker Hub |
| `DOCKER_HUB_TOKEN` | Access token (לא סיסמה!) |
| `HETZNER_HOST` | IP השרת |
| `HETZNER_USER` | משתמש SSH |
| `HETZNER_SSH_KEY` | מפתח SSH פרטי |

הסודות מוזנים ב-`Settings → Secrets and Variables → Actions` ב-GitHub ולא מופיעים בשום לוג.

---

## 13. ניטור

### Prometheus — איסוף מדדים

Prometheus הוא מערכת ניטור open-source שעובדת לפי מודל **pull**: היא מתחברת ל-endpoint `/metrics` של כל שירות ב-interval קבוע (15 שניות) ושומרת את המדדים ב-time-series database.

```yaml
scrape_configs:
  - job_name: "smartrecipe-backend"
    static_configs:
      - targets: ["backend:5000"]
    metrics_path: "/metrics"
```

### prometheus-flask-exporter — מדדים אוטומטיים

הספרייה `prometheus-flask-exporter` מוסיפה לכל endpoint של Flask את המדדים הבאים אוטומטית:

| מדד | תיאור |
|---|---|
| `flask_http_request_total` | מספר כולל של בקשות לפי status, method, path |
| `flask_http_request_duration_seconds` | histogram של זמני תגובה |
| `flask_http_request_exceptions_total` | בקשות שגרמו ל-exception |

### Grafana — ויזואליזציה

Grafana מציג את המדדים של Prometheus כגרפים ולוחות מחוונים.

**Dashboard שנוצר מראש (`smartrecipe.json`):**
- **HTTP Request Rate** — קצב בקשות לפי endpoint בזמן אמת
- **p95 Latency** — זמן תגובה של 95th percentile
- **Total Requests** — counter מצטבר
- **Error Rate** — שגיאות 5xx לשנייה

### Grafana Provisioning — Configuration as Code

```yaml
# datasources/prometheus.yml
datasources:
  - name: Prometheus
    type: prometheus
    url: http://prometheus:9090
    isDefault: true
```

```yaml
# dashboards/dashboards.yml
providers:
  - type: file
    options:
      path: /etc/grafana/provisioning/dashboards
```

Grafana נטען עם datasource ו-dashboard מוגדרים מראש — לא צריך הגדרה ידנית לאחר `docker compose up`.

---

## 14. אבטחה

### עקרונות אבטחה שיושמו

#### 1. הפרדת רשתות
MySQL חשוף **רק** לתוך ה-Docker network הפנימי. Flask אינו חשוף לציבור — Nginx בלבד מגיש את ה-Port 80.

#### 2. Environment Variables לסודות
```yaml
# docker-compose.yml
environment:
  GEMINI_API_KEY: ${GEMINI_API_KEY}
  MYSQL_PASSWORD: ${MYSQL_PASSWORD}
```
סודות לא מוטמעים ב-Dockerfile או בקוד — מועברים ב-runtime מ-`.env` (שב-`.gitignore`).

#### 3. GitHub Secrets
מפתחות Docker Hub ו-SSH נשמרים ב-GitHub Secrets ולא נחשפים ב-logs.

#### 4. Security Headers ב-Nginx
```nginx
add_header X-Frame-Options "SAMEORIGIN";
add_header X-Content-Type-Options "nosniff";
add_header X-XSS-Protection "1; mode=block";
```

#### 5. SQLAlchemy ORM
שימוש ב-ORM מונע SQL Injection — שאילתות מפורמטות עם parameterized queries.

#### 6. Firewall (UFW)
רק פורטים הכרחיים פתוחים (80, 443, SSH, 3000, 9090).

---

## 15. בדיקות

### אסטרטגיית הבדיקות

הבדיקות מחולקות לשתי קטגוריות:

#### test_db.py — בדיקות בסיס נתונים

בדיקות אלה מוודאות שה-ORM וה-MySQL עובדים כהלכה:

| בדיקה | תיאור |
|---|---|
| `test_insert_recipe` | יצירת רשומה וווידוא שקיבלה ID |
| `test_retrieve_recipe` | שמירה ואחזור לפי שדה |
| `test_update_recipe` | עדכון שדה ווידוא הנתונים החדשים |
| `test_delete_recipe` | מחיקה ווידוא היעלמות הרשומה |
| `test_recipe_to_dict` | בדיקת ה-serialization method |

#### test_api.py — בדיקות REST API

בדיקות אלה מוודאות שה-HTTP endpoints עובדים נכון:

| בדיקה | תיאור |
|---|---|
| `test_health_endpoint` | GET /health מחזיר 200 |
| `test_list_recipes_empty` | GET /api/recipes מחזיר JSON תקין |
| `test_save_recipe` | POST יוצר רשומה ומחזיר 201 |
| `test_get_recipe` | GET /:id מחזיר את הרשומה הנכונה |
| `test_update_recipe` | PUT מעדכן שדה |
| `test_delete_recipe` | DELETE מוחק ומחזיר 404 לאחר מכן |
| `test_save_recipe_missing_field` | POST ללא שדה חובה מחזיר 400 |

### Fixtures

```python
@pytest.fixture(scope="session")
def app():
    # יוצר DB tables לפני הסשן
    _db.create_all()
    yield application
    # מוחק הכל בסוף
    _db.drop_all()
```

`scope="session"` — הDB נוצר פעם אחת לכל ריצת pytest, לא לכל בדיקה → ביצועים טובים יותר.

### כיסוי קוד

```bash
pytest --cov=app --cov-report=xml
```

דוח כיסוי (`coverage.xml`) מועלה ל-Codecov לניטור over time.

---

## 16. סיכום

### מה הושג בפרויקט

| תחום | מה נבנה |
|---|---|
| **Backend** | Flask REST API עם 8 endpoints, ORM, Migrations |
| **Frontend** | SPA בסיסי עם JavaScript טהור |
| **Database** | MySQL 8.0 עם schema מוגדר |
| **AI** | אינטגרציית Gemini 1.5 Flash ליצירת מתכונים |
| **Containers** | 5 services ב-Docker Compose |
| **CI/CD** | 3-job pipeline: Test → Build → Deploy |
| **Infrastructure** | Scripts להכנת Hetzner + deployment |
| **Monitoring** | Prometheus + Grafana עם dashboard מוגדר מראש |
| **Tests** | 14 בדיקות pytest (DB + API) |
| **Docs** | README מקצועי + ספר פרויקט בעברית |

### לקחים עיקריים

1. **GitOps עובד:** כל שינוי עובר דרך Git → pipeline → ייצור. אין שינויים ידניים.
2. **Environment Variables חיוניים:** אף סוד לא מוטמע בקוד.
3. **Healthchecks מונעים בעיות:** ללא healthcheck, שירותים יעלו לפני שתלויותיהם מוכנות.
4. **Real DB בבדיקות:** בדיקות שמתחברות ל-MySQL אמיתי תופסות בעיות שmock לא יתפוס.
5. **Monitoring מהיום הראשון:** קל יותר לבנות ניטור בתחילת פרויקט מאשר להוסיפו בהמשך.

### כיוונים עתידיים

- **HTTPS** — הוספת Let's Encrypt/Certbot ל-Nginx
- **Authentication** — JWT tokens לניהול משתמשים
- **Kubernetes** — מעבר מ-Docker Compose ל-k8s לסקיילינג
- **Redis** — Cache לתוצאות Gemini שנוצרו לאחרונה
- **Rate Limiting** — הגבלת קריאות ל-Gemini API לפי משתמש

---

*ספר פרויקט זה נכתב כחלק מפרויקט הסיום בקורס DevOps Engineering.*  
*הקוד המלא זמין ב-GitHub: [github.com/dshrppury/devops-final-project](https://github.com/dshrppury/devops-final-project)*
