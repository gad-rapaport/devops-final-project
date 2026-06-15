# SmartRecipe AI — מדריך הרצה בעברית

## מה בנינו?

**SmartRecipe AI** היא אפליקציית ווב שמייצרת מתכונים בעזרת בינה מלאכותית.

המשתמש מכניס מרכיבים שיש לו בבית (עגבנייה, עוף, שום...) וה-AI של Google (Gemini) מחזיר מתכון מלא עם הוראות הכנה, זמן בישול, ומידע תזונתי. אפשר לשמור מתכונים, לדרג אותם, ולמחוק.

---

## ארכיטקטורת המערכת — מה רץ על מה

```
אתה (דפדפן)
      │
      ▼
  Nginx :80        ← שרת קבצים סטטיים + Reverse Proxy
      │
      ▼
  Flask :5000      ← Python backend, לוגיקה, API
      │
      ├──▶  MySQL :3306     ← בסיס הנתונים (מתכונים שמורים)
      │
      └──▶  Gemini API      ← AI של Google (בענן, חיצוני)

  Prometheus :9090  ← איסוף מדדים מה-Flask
  Grafana    :3000  ← גרפים ולוחות מחוונים
```

כל אחד מהרכיבים האלה רץ בתוך **Docker container** נפרד.  
**Docker Compose** מנהל את כולם יחד בפקודה אחת.

---

## קבצים חשובים בפרויקט

```
devops-final-project/
│
├── backend/                  ← שרת Python (Flask)
│   ├── app/
│   │   ├── __init__.py       ← יצירת האפליקציה
│   │   ├── models.py         ← מבנה טבלת המתכונים ב-DB
│   │   ├── routes/
│   │   │   ├── recipes.py    ← כל ה-API endpoints (CRUD + AI)
│   │   │   └── health.py     ← /health endpoint
│   │   └── services/
│   │       └── gemini_service.py  ← קוד שמדבר עם Gemini AI
│   ├── tests/                ← בדיקות אוטומטיות
│   ├── requirements.txt      ← תלויות Python
│   └── Dockerfile            ← איך לבנות את ה-container של Flask
│
├── frontend/
│   ├── nginx.conf            ← הגדרות Nginx (proxy + קבצים סטטיים)
│   ├── Dockerfile            ← איך לבנות את ה-container של Nginx
│   └── html/index.html       ← כל ממשק המשתמש (HTML+CSS+JS)
│
├── monitoring/
│   ├── prometheus/           ← הגדרות איסוף מדדים
│   └── grafana/              ← dashboard מוכן מראש
│
├── infrastructure/
│   ├── hetzner_setup.sh      ← סקריפט להכנת שרת Hetzner חדש
│   └── deploy.sh             ← סקריפט לעדכון הגרסה בשרת
│
├── .github/workflows/
│   └── ci-cd.yml             ← Pipeline אוטומטי (GitHub Actions)
│
├── docker-compose.yml        ← הרצה מקומית (dev)
├── docker-compose.prod.yml   ← override לייצור (משתמש ב-Docker Hub)
└── .env.example              ← דוגמה לקובץ הסודות
```

---

## איך מריצים — שלב אחר שלב

### דרישות מוקדמות

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) — חייב להיות מותקן ורץ
- מפתח Gemini API — מקבלים בחינם בכתובת: https://aistudio.google.com/app/apikey

---

### שלב 1 — שכפול הקוד מ-GitHub

פתח Terminal (PowerShell או CMD) והרץ:

```bash
git clone https://github.com/gad-rapaport/devops-final-project.git
cd devops-final-project
```

---

### שלב 2 — יצירת קובץ הסודות (.env)

```bash
copy .env.example .env
```

פתח את הקובץ `.env` בעורך (Notepad/VS Code) ומלא:

```env
MYSQL_ROOT_PASSWORD=בחר_סיסמה_חזקה
MYSQL_PASSWORD=בחר_סיסמה_נוספת
SECRET_KEY=מחרוזת_אקראית_ארוכה_לפחות_32_תווים
GEMINI_API_KEY=הכנס_כאן_את_המפתח_שלך_מ_Google
DOCKER_HUB_USERNAME=שם_המשתמש_שלך_ב_Docker_Hub
GF_ADMIN_USER=admin
GF_ADMIN_PASSWORD=בחר_סיסמה_ל_Grafana
```

> **חשוב:** את הקובץ `.env` **אסור** להעלות ל-GitHub. הוא כבר ב-`.gitignore`.

---

### שלב 3 — הרצת כל המערכת

```bash
docker compose up -d --build
```

הפקודה הזאת:
1. בונה את ה-Docker images של Flask ו-Nginx
2. מורידה את images של MySQL, Prometheus, Grafana
3. מפעילה את כל 5 ה-containers

זה ייקח כ-2-3 דקות בפעם הראשונה (הורדת images).

---

### שלב 4 — יצירת טבלאות בבסיס הנתונים

```bash
docker compose exec backend flask db upgrade
```

זה יוצר את טבלת `recipes` ב-MySQL.

---

### שלב 5 — פתח את האפליקציה

| שירות | כתובת | פרטי כניסה |
|---|---|---|
| **האפליקציה** | http://localhost | — |
| **Grafana** | http://localhost:3000 | admin / מה שהגדרת ב-.env |
| **Prometheus** | http://localhost:9090 | — |

---

## איך משתמשים באפליקציה

1. **מכניסים מרכיבים** — מקלידים מרכיב ולוחצים Enter (למשל: עוף, לימון, שום)
2. **לוחצים "Generate Recipe"** — Gemini AI מייצר מתכון מלא
3. **שומרים** — לוחצים "Save Recipe" לשמירה ב-MySQL
4. **רשימת מתכונים** — מימין מוצגים כל המתכונים השמורים
5. **לחיצה על מתכון** — פותח פרטים מלאים עם אפשרות מחיקה

---

## פקודות שימושיות

```bash
# הצגת logs של שירות מסוים
docker compose logs backend -f
docker compose logs frontend -f

# עצירת הכל
docker compose down

# עצירת הכל + מחיקת נתונים (זהירות!)
docker compose down -v

# הפעלה מחדש של שירות ספציפי
docker compose restart backend

# כניסה לתוך ה-container של Flask
docker compose exec backend bash

# כניסה ל-MySQL
docker compose exec db mysql -u smartrecipe -p smartrecipe
```

---

## CI/CD Pipeline — GitHub Actions

כל `git push` לענף `main` מפעיל אוטומטית:

```
1. בדיקות pytest (מול MySQL אמיתי)
        ↓
2. בנייה של Docker images + העלאה ל-Docker Hub
        ↓
3. SSH לשרת Hetzner + עדכון הגרסה
```

### להפעיל את ה-Pipeline צריך להוסיף Secrets ב-GitHub:

כנס לכתובת:  
`https://github.com/gad-rapaport/devops-final-project/settings/secrets/actions`

ולהוסיף:

| שם ה-Secret | מה להכניס |
|---|---|
| `DOCKER_HUB_USERNAME` | שם המשתמש שלך ב-Docker Hub |
| `DOCKER_HUB_TOKEN` | Access Token מ-Docker Hub (לא סיסמה) |
| `HETZNER_HOST` | ה-IP של שרת Hetzner שלך |
| `HETZNER_USER` | `root` (או `deploy`) |
| `HETZNER_SSH_KEY` | התוכן המלא של `~/.ssh/id_ed25519` (המפתח הפרטי) |
| `GEMINI_API_KEY` | מפתח Gemini שלך |

---

## Hetzner — שרת ייצור

יש לך שרת Hetzner קיים על `116.203.217.113`.

להכין אותו בפעם הראשונה:

```bash
# 1. התחבר לשרת
ssh root@116.203.217.113

# 2. הרץ את סקריפט ההכנה
bash <(curl -fsSL https://raw.githubusercontent.com/gad-rapaport/devops-final-project/main/infrastructure/hetzner_setup.sh)

# 3. צור את קובץ הסודות
nano /opt/smartrecipe/.env
# (מלא כמו בשלב 2 למעלה)

# 4. העתק קבצי Compose לשרת (מהמחשב המקומי שלך)
scp docker-compose.yml docker-compose.prod.yml root@116.203.217.113:/opt/smartrecipe/
scp -r monitoring/ infrastructure/ root@116.203.217.113:/opt/smartrecipe/

# 5. הרץ
cd /opt/smartrecipe
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

לאחר הגדרת GitHub Secrets, כל push יפרוס אוטומטית לשרת הזה.

---

## בדיקות — pytest

הבדיקות בודקות 2 דברים:
1. **`test_db.py`** — הכנסה, שליפה, עדכון ומחיקה של מתכונים ב-MySQL
2. **`test_api.py`** — כל ה-API endpoints (GET, POST, PUT, DELETE)

```bash
# הרצת בדיקות מקומית (דורש MySQL על פורט 3307)
docker compose up -d db
docker compose exec \
  -e TEST_DATABASE_URL=mysql+pymysql://smartrecipe:smartrecipe@db:3306/smartrecipe_test \
  backend pytest -v
```

---

## ניטור — Prometheus + Grafana

- **Prometheus** מתחבר כל 15 שניות ל-`/metrics` של Flask ושומר נתוני ביצועים
- **Grafana** מציג גרפים של: מספר בקשות, זמן תגובה, שגיאות

Dashboard מוכן מראש נטען אוטומטית בכניסה ל-Grafana.

---

## שאלות נפוצות

**ה-container של backend נופל — מה לעשות?**
```bash
docker compose logs backend
# בדרך כלל בגלל שה-DB עדיין לא מוכן — המתן 30 שניות ונסה שוב
docker compose restart backend
```

**שכחתי להריץ את המיגרציה**
```bash
docker compose exec backend flask db upgrade
```

**רוצה לראות את המתכונים ישירות ב-DB**
```bash
docker compose exec db mysql -u smartrecipe -psmartrecipe smartrecipe -e "SELECT id, title, cuisine_type, created_at FROM recipes;"
```

**רוצה לאפס הכל ולהתחיל מחדש**
```bash
docker compose down -v
docker compose up -d --build
docker compose exec backend flask db upgrade
```
