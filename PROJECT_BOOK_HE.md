# ספר פרויקט גמר

---

**שם הפרויקט: SmartRecipe AI — מחולל מתכונים חכם**

**שם הסטודנט:** dshrppury (gad-rapaport)

**שם המנחה:** —

**מסלול:** הנדסאי תוכנה / DevOps

**תאריך:** יוני 2026

---

## תוכן עניינים

1. [רקע — DevOps מהו](#1-רקע--devops-מהו)
2. [היסטוריה — מונוליט לעומת מיקרו-שירותים](#2-מונוליט-לעומת-מיקרו-שירותים)
3. [מטרת הפרויקט](#3-מטרת-הפרויקט)
4. [סקירת מצב קיים בשוק](#4-סקירת-מצב-קיים-בשוק)
5. [מה הפרויקט מחדש ומשפר](#5-מה-הפרויקט-מחדש-ומשפר)
6. [דרישות מערכת ופונקציונליות](#6-דרישות-מערכת)
7. [בעיות צפויות ופתרונות](#7-בעיות-צפויות-ופתרונות)
8. [טכנולוגיות בשימוש](#8-טכנולוגיות-בשימוש)
9. [תיאור הפרויקט](#9-תיאור-הפרויקט)
10. [מהכלל אל הפרט — האפליקציה](#10-מהכלל-אל-הפרט)
11. [שכבת ה-Frontend — Nginx](#11-שכבת-ה-frontend--nginx)
12. [שכבת ה-Backend — Python Flask](#12-שכבת-ה-backend--python-flask)
13. [שכבת ה-SQL — MySQL](#13-שכבת-ה-sql--mysql)
14. [אינטגרציית AI — Gemini](#14-אינטגרציית-ai--gemini)
15. [אריזה בדוקר — Docker Compose](#15-אריזה-בדוקר)
16. [תהליך ה-CI/CD — GitHub Actions](#16-תהליך-ה-cicd)
17. [עקרונות Git ו-CI/CD בפרויקט](#17-עקרונות-git-ו-cicd)
18. [תשתית הענן — Hetzner](#18-תשתית-הענן--hetzner)
19. [ניטור — Prometheus ו-Grafana](#19-ניטור)
20. [אבטחת הפייפליין — Secrets](#20-אבטחת-הפייפליין--secrets)
21. [בדיקות — pytest](#21-בדיקות--pytest)
22. [שאלות צפויות מהבוחן](#22-שאלות-צפויות-מהבוחן)
23. [סיכום](#23-סיכום)

---

## 1. רקע — DevOps מהו

דבאופס זאת גישת פיתוח, תפעול וניהול תוכנה הדוגלת בביזור ופיצול תהליכים ושירותים, הפשטת החומרה מן התוכנה והנגשתה, פיתוח ושחרור מהיר של גרסאות ואוטומציה בעזרת כלים ושיטות עבודה חדשניות וניצול ושילוב תשתיות ענן.

המילה "DevOps" היא שילוב של שתי מילים: **Development** (פיתוח) ו-**Operations** (תפעול). בעולם המסורתי, צוותי הפיתוח וצוותי התפעול עבדו בנפרד, כאשר כל צד לא הבין לחלוטין את הצד האחר — המפתח לא הכיר את השרת, ואנשי התפעול לא הבינו את הקוד. גישת ה-DevOps פורצת מחיצה זו וגורמת לשני הצוותים לעבוד יחד, לחלוק אחריות ולאוטמט את כל מה שניתן.

המטרה המרכזית: **להוציא גרסאות תוכנה חדשות לייצור מהר, בטוח, ובאופן אוטומטי.**

```
Plan → Code → Build → Test → Release → Deploy → Operate → Monitor
  └─────────────────────────── לולאה מתמשכת ──────────────────────┘
```

---

## 2. מונוליט לעומת מיקרו-שירותים

### גישת המונוליט (Monolith)

פיתוח בחבילה אחת גדולה המכילה את כל הספריות, הרכיבים והשירותים. התוצאה הייתה קוד ענקי שצוות התפעול (Operations) קיבל בכל גרסה חדשה — כשהוא מבין בחומרה אך לא בתוכנה.

**חסרונות עיקריים:**

- פיתוח מסורבל — כל הרכיבים חייבים להיכתב באותה שפה
- איתור באגים קשה עקב גודל הקוד
- סקיילינג של רכיב אחד מחייב שדרוג של כל המערכת — בזבוז משאבים
- קשיי התאמה לפלטפורמות שונות

### גישת המיקרו-שירותים (Microservices)

כל רכיב ושירות הוא תוכנה קטנה עצמאית, המחוברת לאחרים דרך ממשקי API.

**יתרונות:** כל שירות בשפה משלו, סקיילינג עצמאי, איתור בעיות פשוט יותר, פריסה עצמאית לכל שירות.

**חסרונות:** מורכבות תפעולית גבוהה, צורך בכלי Orchestration, יותר נקודות כשל פוטנציאליות, עלות הקמה גבוהה יותר.

### הפרויקט הנוכחי — ארכיטקטורה היברידית

הפרדה לשירותים נפרדים (Frontend, Backend, Database, Monitoring) שכל אחד רץ בקונטיינר Docker נפרד, אך הלוגיקה הפנימית של ה-Backend נכתבה כמונוליט מפושט. זוהי הגישה האופטימלית לפרויקט בסדר גודל זה — מורכבות ניהולית נמוכה עם הפרדה ברורה בין שכבות.

---

## 3. מטרת הפרויקט

הפרויקט הינו הצגת תורת ה-DevOps דרך הדמיית תהליך פיתוח תוכנה, פריסתה והרצתה (Deployment) תוך שימוש בכמה מן הטכנולוגיות העולות והחדישות ביותר, והצגת המערך כולו על שרת ענן.

הפרויקט משלב:
- **אפליקציית ווב שימושית** — מחולל מתכונים המשתמש ב-Gemini AI של Google
- **מערך DevOps מלא** — מ-Commit ועד Deployment אוטומטי
- **ניטור ובקרה** — Prometheus + Grafana לניטור ביצועים בזמן אמת

---

## 4. סקירת מצב קיים בשוק

כיום יותר ויותר חברות עוברות להטמעת תורת ה-DevOps ברמות שונות. קמות יותר ויותר חברות ייעוץ ותפעול על טהרת ה-DevOps. ישנן חברות המשווקות ומתפעלות שירותים לאורקסטרציה, ניהול ותפעול קונטיינרים.

בנוסף, בעידן ה-AI הגנרטיבי, מודלי שפה גדולים (LLM) כמו Gemini של Google ו-GPT של OpenAI הופכים לחלק אינטגרלי ממוצרי תוכנה. היכולת לשלב AI בפייפליין DevOps רגיל — כולל בדיקות, Docker, ו-CI/CD — היא כישור קריטי בשוק העבודה כיום.

---

## 5. מה הפרויקט מחדש ומשפר

- **שילוב AI בפייפליין DevOps** — הפרויקט מדגים כיצד לשלב קריאות לממשקי AI (Gemini API) בתוך אפליקציה המנוהלת ב-CI/CD מלא.
- **Git כמקור האמת לקוד ולקונפיגורציה** — הפרויקט מיישם עקרונות GitOps, שבהם כל שינוי קוד וקונפיגורציה עובר דרך Git ומפעיל את הפייפליין האוטומטי.
- **אוטומציית תשתית באמצעות סקריפטי Bash** — סקריפטים לאוטומציה מלאה של הכנת השרת ופריסת האפליקציה.
- **Monitoring מובנה** — Prometheus ו-Grafana משולבים מהיום הראשון עם dashboard מוגדר מראש.
- **ניהול סודות נכון** — GitHub Secrets ו-Environment Variables לניהול פריטים רגישים.

---

## 6. דרישות מערכת

**דרישות לסביבת הרצה מקומית:**
- Docker Desktop (גרסה 24+) + Docker Compose v2
- Git
- מפתח Gemini API (חינמי) מ-https://aistudio.google.com/app/apikey

**דרישות לסביבת ייצור:**
- שרת Hetzner Cloud עם Ubuntu 22.04 (VPS)
- חשבון Docker Hub (לאחסון Images)
- חשבון GitHub (לניהול קוד ו-CI/CD)
- מפתח SSH מוגדר

**פונקציונליות האפליקציה:**
- הזנת רשימת מרכיבים וקבלת מתכון שלם מ-AI
- שמירה, עדכון ומחיקה של מתכונים
- פילטור מתכונים לפי סוג מטבח
- קבלת הצעות שינוי למתכון מ-AI
- ממשק ויזואלי נוח ונגיש

---

## 7. בעיות צפויות ופתרונות

**בעיה: בעת עדכון ושינוי קבצי המקור יכולים להיווצר באגים, ועם קצב עדכונים מהיר, האפליקציה יכולה ליפול.**

פתרון: הרצת בדיקות תוכנה (pytest) על כל שינוי בקוד — מהירות ואיתור בעיות מוקדם הינו חלק מרכזי מהמערכת. הפייפליין עוצר אוטומטית אם בדיקה נכשלת ושולח מייל.

**בעיה: תלות בין שירותים — Flask שעולה לפני ש-MySQL מוכן.**

פתרון: Docker healthcheck על MySQL + `depends_on: condition: service_healthy` מבטיח שה-Backend עולה רק לאחר שה-DB מוכן לחלוטין.

**בעיה: חשיפת סודות (API keys, סיסמאות) בקוד.**

פתרון: שימוש ב-Environment Variables, קובץ `.env` שב-`.gitignore`, ו-GitHub Secrets לפייפליין. אף סוד לא מופיע בקוד המקור.

**בעיה: פריצה לאחד הרכיבים מאפשרת גישה למערכת כולה.**

פתרון: רק Nginx חשוף לאינטרנט (פורט 80). Flask ו-MySQL נמצאים ברשת Docker פנימית בלבד ואינם נגישים ישירות מהאינטרנט.

**בעיה: קריאות ל-Gemini AI עלולות להיכשל או לקחת זמן.**

פתרון: Gunicorn עם timeout של 120 שניות + טיפול ב-exceptions. במקרה של כשל בשירות Gemini (rate limit, רשת, תקלה), מוחזרת הודעת שגיאה ידידותית למשתמש (`HTTP 500` עם הסבר) והשגיאה נרשמת ב-logs לצורך תחקור. אין Fallback למתכון מוכן מראש — הודעת השגיאה מזמינה את המשתמש לנסות שוב.

---

## 8. טכנולוגיות בשימוש

### קונטיינר (Container)
קונטיינר הינו יחידה המדמה סביבה נפרדת וסטרילית במחשב — מעין מחשב בתוך מחשב. מה שמופעל בתוכו אינו מודע לתהליכים הרצים מחוצה לו. בניגוד למכונה וירטואלית, קונטיינר חולק את ליבת מערכת ההפעלה (Kernel) עם המחשב המארח, ובכך משתמש בפחות משאבים ויעיל יותר.

### Image (אימג')
האימג' הינו מערכת הקבצים הפועלת בתוך הקונטיינר. הוא מורכב מכל הקבצים הנדרשים — מרמת מערכת ההפעלה ועד התהליך עצמו (האפליקציה). ניתן לדמות אימג' לכונן הקשיח של הקונטיינר.

### Registry (רגיסטרי)
מקום אחסון לאימג'ים, מקוטלג לפי שם האימג' וגרסה. בפרויקט זה נעשה שימוש ב-**Docker Hub** כרגיסטרי ציבורי/פרטי. כל push לענף main מעלה image חדש לרגיסטרי עם שני תגים: `:latest` ו-`:sha-<hash>` לאפשרות Rollback.

### Docker
תוכנה, ממשק ליצירה, ניהול, החלפה ומחיקה של קונטיינרים. מאפשר יצירת רשתות וירטואליות לחיבור קונטיינרים, חיבור לרשת המחשב המארח, והכנסת מידע לקונטיינרים על ידי Volumes. ניתן להריץ קונטיינרים מאימג'ים שאינם מקומיים על ידי ציון שם הרגיסטרי.

### Docker Compose
כלי לניהול מספר קונטיינרים במקביל על ידי קובץ YAML אחד. בפרויקט זה ה-Compose מנהל 5 שירותים: Nginx, Flask, MySQL, Prometheus, ו-Grafana. ה-Compose מגדיר את הרשתות, ה-Volumes, ה-healthchecks וסדר ההפעלה.

### Git ו-GitHub
**Git** — מערכת מקומית לשמירת קבצי מקור, היסטוריה וגרסאות שלהם. מאפשר מעקב אחר שינויים וחזרה לגרסאות קודמות.

**GitHub** — שירות ציבורי הפועל באינטגרציה מלאה עם Git. בפרויקט לגיטהאב מקום מרכזי שכן הינו הטריגר לתהליך ה-CI/CD — על כל שינוי בקוד, GitHub Actions מופעל אוטומטית.

### GitHub Actions
כלי ל-CI/CD המשולב בגיטהאב. מאפשר בנייה, הפעלה ואוטומציית תהליך ה-CI/CD. בפרויקט מחליף את Jenkins — על כל עדכון קבצי המקור, ה-Workflow מופעל ובאמצעותו נבנה התוצר הסופי, מתבצעות בדיקות, ובסופו מתבצע עדכון גרסה ופריסה אוטומטית לשרת.

### Nginx (אנג'ין-איקס)
שרת Frontend ו-Reverse Proxy המאפשר אחסון קבצי ה-Frontend של האפליקציה וכך להוריד עומס ולספק שכבת הגנה נוספת לאפליקציה שהינה Backend. בפרויקט ממלא שני תפקידים: (1) מגיש קבצי HTML/CSS/JS סטטיים, (2) מנתב בקשות `/api/*` לשרת Flask הפנימי.

### Python + Flask
**Python** — שפת תכנות מפורשת (Interpreted) המשמשת לכתיבת ה-Backend. גמישה, קריאה, ובעלת ספריות עשירות לעבודה עם בסיסי נתונים, ממשקי API, ו-AI.

**Flask** — מיקרו-פריימוורק ל-Python לבניית REST API. קל, מודולרי, ומאפשר בנייה מהירה של שרת Backend עם endpoints ברורים.

### MySQL
שרת אחסון נתונים בטבלאות (Relational Database). בפרויקט מאחסן את כל המתכונים השמורים. מנוהל דרך SQLAlchemy ORM ו-Flask-Migrate לביצוע Migrations בצורה מסודרת ובטוחה.

### Gemini AI
מודל שפה גדול (LLM) של Google. בפרויקט נעשה שימוש ב-**gemini-1.5-flash** — גרסה מהירה, יעילה ובעלת יכולות מצוינות ליצירת טקסט מובנה. משמש ליצירת מתכונים מפורטים בפורמט JSON על בסיס רשימת מרכיבים שהמשתמש מספק.

### Prometheus
מערכת ניטור open-source העובדת לפי מודל pull — מתחברת ל-`/metrics` של כל שירות כל 15 שניות ושומרת נתוני ביצועים ב-time-series database. מודד: מספר בקשות HTTP, זמני תגובה, שגיאות.

### Grafana
כלי ויזואליזציה לנתוני Prometheus. מציג גרפים ולוחות מחוונים (Dashboards) בזמן אמת. בפרויקט מוגדר מראש (Provisioning) עם datasource ו-Dashboard אוטומטיים.

### Hetzner Cloud
ספק שרתי ענן אירופי. בפרויקט משמש כסביבת הייצור — שרת VPS על Ubuntu 22.04. בחירה ב-Hetzner על פני AWS/GCP מאפשרת חיסכון בעלויות תוך שמירה על כל יכולות ה-DevOps.

---

## 9. תיאור הפרויקט

הפרויקט הינו מודל DevOps המדגים תהליך מלא מרמת כתיבת קוד ועד פריסה בייצור. לשם כך, נבנתה אפליקציית ווב שימושית — **SmartRecipe AI**.

**האפליקציה:** המשתמש מכניס מרכיבים שיש לו בבית (עגבנייה, עוף, שום...) ו-Gemini AI מייצר מתכון מלא עם הוראות, זמן הכנה, מידע תזונתי וסוג מטבח. המתכונים נשמרים ב-MySQL ומוצגים ברשימה עם אפשרות דירוג ומחיקה.

**המערך האוטומטי:** על כל שינוי קוד ש-push לגיטהאב — מתחיל תהליך CI/CD אוטומטי: בדיקות pytest מול MySQL אמיתי, בנייה והעלאה של Docker images לDocker Hub, ופריסה אוטומטית לשרת ה-Hetzner.

**תרשים תהליך:**

```
Developer pushes code
         │
         ▼
   GitHub (main branch)
         │  triggers
         ▼
  GitHub Actions Workflow
    ┌────────────────────────────────┐
    │  Job 1: TEST                   │
    │  • הרמת MySQL container        │
    │  • pip install                 │
    │  • pytest -v (14 בדיקות)       │
    │  • מייל על כשלון               │
    └────────────┬───────────────────┘
                 │ pass
    ┌────────────▼───────────────────┐
    │  Job 2: BUILD & PUSH           │
    │  • docker buildx               │
    │  • push :latest + :sha-<hash>  │
    │    → Docker Hub                │
    │  • מייל על כשלון               │
    └────────────┬───────────────────┘
                 │
    ┌────────────▼───────────────────┐
    │  Job 3: DEPLOY                 │
    │  • SCP compose files           │
    │  • SSH → Hetzner               │
    │  • docker compose pull         │
    │  • docker compose up -d        │
    │  • מייל הצלחה / כשלון          │
    └────────────────────────────────┘
```

**המערכת כולה אוטומטית** — לאחר ה-Push, אין מגע ידני עד שהאפליקציה החדשה עולה בשרת הייצור.

---

## 10. מהכלל אל הפרט

### האפליקציה

האפליקציה שנכתבה הינה מחולל מתכונים חכם (SmartRecipe AI) בה המשתמש יכול לגשת לאתר, להכניס רשימת מרכיבים ולקבל מתכון מפורט בעזרת בינה מלאכותית. המתכונים נשמרים, ניתן לצפות בהם, לדרג אותם ולמחוק. הניתוב באפליקציה מתבצע בממשק REST API.

### חלקי האפליקציה

**1. בסיס נתונים (Database) — MySQL**
מאחסן את כל המתכונים שהמשתמש שמר. כל מתכון כולל: כותרת, מרכיבים, הוראות הכנה, מידע תזונתי, סוג מטבח, זמן הכנה, דירוג, ותאריך יצירה.

**2. Backend — Python Flask**
המנוע של האפליקציה. מעבד בקשות HTTP, מתקשר עם ה-DB, קורא ל-Gemini AI ומחזיר תשובות ב-JSON. נכתב בפייתון עם פריימוורק Flask.

**3. Frontend — Nginx + HTML/JS**
שרת קדמי בו מאוחסנים קבצי האתר המוצגים למשתמש, ומשמש כ-Reverse Proxy לבאקאנד. אחראי על הניתוב בהתאם לכתובת URL ומשמש כמגן-סף לשרת Flask.

הפרונט הינו **החלק היחידי החשוף לאינטרנט**. Flask ו-MySQL נמצאים מאחורי Nginx ברשת פנימית בלבד:

```
אינטרנט (WWW)
      │
      ▼
  Nginx :80          ← פרונט, שרת קבצים + Reverse Proxy
      │                  גלוי לאינטרנט
      ▼
  Flask :5000        ← Backend, לוגיקה
      │                  ברשת Docker פנימית בלבד
      ▼
  MySQL :3306        ← Database
                        ברשת Docker פנימית בלבד
```

---

## 11. שכבת ה-Frontend — Nginx

### תפקידי Nginx בפרויקט

**File Server (שרת קבצים):**
Nginx מגיש ישירות את קבצי ה-HTML, CSS, ו-JavaScript לדפדפן המשתמש ללא מגע של Flask. זה חוסך עומס מה-Python server ומאפשר ל-Flask להתמקד בלוגיקה העסקית בלבד.

**Reverse Proxy:**
כל בקשה שמגיעה ל-`/api/*` מנותבת על ידי Nginx לשרת Flask הפנימי:

```nginx
location /api/ {
    proxy_pass http://backend:5000;
    proxy_read_timeout 120s;
}
```

ה-timeout של 120 שניות חשוב — קריאות ל-Gemini AI עשויות לקחת עד 15-30 שניות.

**Load Balancing:**
ה-`upstream` block ב-nginx.conf מאפשר הוספת מספר instances של Flask בעתיד:
```nginx
upstream backend {
    server backend:5000;
    # server backend2:5000;  # ← ניתן להוסיף
}
```

**Security Headers:**
Nginx מוסיף headers שמגנים מפני XSS, Clickjacking ו-MIME sniffing.

### ממשק המשתמש

ממשק המשתמש נבנה כ-SPA (Single Page Application) בוונילה JavaScript ללא frameworks. כולל:
- **Tag Input** — הזנת מרכיבים כתגיות עם Enter
- **AI Generator Panel** — הצגת המתכון שנוצר על ידי Gemini
- **Recipe List** — רשימה ממוספרת עם pagination
- **Modal** — פרטי מתכון מלאים

---

## 12. שכבת ה-Backend — Python Flask

### App Factory Pattern

```python
def create_app(config=None):
    app = Flask(__name__)
    db.init_app(app)
    migrate.init_app(app, db)
    metrics.init_app(app)   # Prometheus
    CORS(app)
    app.register_blueprint(recipes_bp, url_prefix="/api")
    app.register_blueprint(health_bp)
    return app
```

ה-App Factory Pattern מאפשר יצירת instances שונים של האפליקציה (dev, test, prod) — חיוני לבדיקות. פונקציית `create_app()` מקבלת קונפיגורציה ומחזירה instance מוכן.

### Blueprints — ניתוב מודולרי

| Blueprint | קידומת URL | תיאור |
|---|---|---|
| `health` | `/` | `/health` ו-`/` (index) |
| `recipes` | `/api` | כל פעולות ה-CRUD + AI |

### REST API Endpoints

| Method | Endpoint | תיאור |
|---|---|---|
| GET | `/health` | בדיקת תקינות + סטטוס DB |
| GET | `/api/recipes` | רשימת מתכונים (paginated) |
| GET | `/api/recipes/:id` | מתכון בודד |
| POST | `/api/recipes/generate` | **יצירת מתכון עם Gemini AI** |
| POST | `/api/recipes` | שמירת מתכון |
| PUT | `/api/recipes/:id` | עדכון מתכון |
| DELETE | `/api/recipes/:id` | מחיקת מתכון |
| GET | `/api/recipes/:id/variations` | הצעות שינוי מ-AI |
| GET | `/metrics` | מדדי Prometheus |

### Gunicorn — Production Server

```
gunicorn --bind 0.0.0.0:5000 --workers 4 --timeout 120 wsgi:app
```

Flask dev server אינו מתאים לייצור (single-threaded, ללא process management). Gunicorn מריץ 4 worker processes המאפשרים טיפול בבקשות במקביל. מספר ה-workers נקבע בהתאם לנפח המשאבים של שרת הייצור — הכלל המקובל הוא `(2 × CPU cores) + 1`, ולשרת עם 2 ליבות המשמעות היא 4-5 workers.

---

## 13. שכבת ה-SQL — MySQL

### מבנה הטבלה

```sql
CREATE TABLE recipes (
    id                INT AUTO_INCREMENT PRIMARY KEY,
    title             VARCHAR(255) NOT NULL,
    ingredients       TEXT NOT NULL,
    instructions      TEXT NOT NULL,
    nutritional_info  TEXT,
    cuisine_type      VARCHAR(100),
    prep_time_minutes INT,
    rating            FLOAT DEFAULT 0.0,
    created_at        DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### Flask-Migrate — ניהול Migrations

במקום יצירה ידנית של טבלאות, Flask-Migrate מנהל את השינויים בסכמה בצורה מסודרת:

```bash
flask db migrate -m "add cuisine_type column"
flask db upgrade
```

כל migration נשמר בתיקיית `migrations/` ב-Git, כך שניתן לעקוב אחרי כל שינוי בסכמה.

### SQLAlchemy ORM — הגנה מפני SQL Injection

שימוש ב-ORM (Object Relational Mapper) מונע SQL Injection כיוון שכל שאילתה עוברת דרך parameterized queries אוטומטיות:

```python
# בטוח — ORM מטפל ב-escaping
recipe = Recipe.query.filter_by(title="Pasta").first()

# מסוכן — לעולם לא כך
cursor.execute(f"SELECT * FROM recipes WHERE title = '{user_input}'")
```

### Health Check ו-Volume

```yaml
healthcheck:
  test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
  interval: 10s
  retries: 5

volumes:
  - db_data:/var/lib/mysql
```

ה-healthcheck מבטיח ש-Flask לא מנסה להתחבר לפני ש-MySQL מוכן. ה-Volume מבטיח ששמירת הנתונים קבועה גם לאחר `docker compose down`.

### גיבוי — Backup

חשוב להבחין בין **Volume לבין גיבוי**: Volume מגן מפני מחיקה בעת הורדת קונטיינרים, אך אינו גיבוי — קלקול בדיסק או Volume פגום יגרמו לאיבוד נתונים. לכן, בסביבת הייצור מומלץ להוסיף גיבוי יומי של MySQL באמצעות `mysqldump` לשמירה של 7 ימים אחרונים:

```bash
# cron job יומי — גיבוי MySQL
0 2 * * * docker exec smartrecipe-db \
  mysqldump -u smartrecipe -p"$MYSQL_PASSWORD" smartrecipe \
  > /opt/smartrecipe/backups/recipes_$(date +\%Y\%m\%d).sql
# מחיקת גיבויים ישנים מעבר ל-7 ימים
find /opt/smartrecipe/backups -name "*.sql" -mtime +7 -delete
```

---

## 14. אינטגרציית AI — Gemini

### Prompt Engineering

המפתח לקבלת תגובה מובנית ועקבית מ-Gemini הוא ה-Prompt:

```python
prompt = f"""You are a professional chef and nutritionist.
Generate a detailed recipe using primarily these ingredients: {ingredients_str}.

Respond ONLY with a valid JSON object (no markdown) in this exact structure:
{{
  "title": "Recipe Name",
  "ingredients": "Full ingredient list with quantities",
  "instructions": "Step-by-step cooking instructions",
  "nutritional_info": "Calories, protein, carbs, fat per serving",
  "cuisine_type": "e.g. Italian, Asian",
  "prep_time_minutes": 30
}}"""
```

עקרונות ה-Prompt:
1. **תפקיד ברור** — "Professional chef and nutritionist"
2. **פורמט מוגדר** — JSON בלבד, ללא markdown
3. **מבנה מדויק** — מניעת תגובות לא עקביות
4. **Fallback** — ניקוי אוטומטי של backticks אם Gemini מוסיף

### טיפול בשגיאות Gemini

```python
try:
    recipe_data = generate_recipe(ingredients, preferences)
except Exception as e:
    return jsonify({"error": f"AI generation failed: {str(e)}"}), 500
```

במקרה של כשל (rate limit, timeout, תקלת רשת) — מוחזרת הודעת שגיאה ידידותית ב-HTTP 500 עם הסבר. השגיאה נרשמת ב-logs של Gunicorn לצורך תחקור עתידי. המשתמש מוזמן לנסות שוב — אין Fallback למתכון מוכן מראש כיוון שאפליקציה מסוג זה תלויה מטבעה ב-AI.

### אבטחת ה-API Key

```yaml
# docker-compose.yml
environment:
  GEMINI_API_KEY: ${GEMINI_API_KEY}
```

המפתח מועבר אך ורק כ-Environment Variable — **לעולם לא** בקוד המקור או ב-Git.

---

## 15. אריזה בדוקר

### Dockerfile — Backend

```dockerfile
FROM python:3.12-slim           # image קטן
WORKDIR /app
RUN apt-get install -y \
    default-libmysqlclient-dev gcc pkg-config
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt   # cache layer
COPY . .
CMD ["gunicorn", "--bind", "0.0.0.0:5000", \
     "--workers", "4", "--timeout", "120", "wsgi:app"]
```

### Dockerfile — Frontend

```dockerfile
FROM nginx:1.27-alpine          # image קטן מאוד
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY html/ /usr/share/nginx/html/
EXPOSE 80
```

### docker-compose.yml — כל השירותים

```yaml
services:
  db:         # MySQL 8.0 + healthcheck + volume
  backend:    # Flask, depends_on: db (healthy)
  frontend:   # Nginx, port 80 → world
  prometheus: # מדדים, port 9090
  grafana:    # dashboard, port 3000
```

### docker-compose.prod.yml — Override לייצור

```yaml
services:
  backend:
    image: ${DOCKER_HUB_USERNAME}/smartrecipe-backend:${IMAGE_TAG}
    build: ~   # ← מבטל בנייה, מוריד מ-Registry
  frontend:
    image: ${DOCKER_HUB_USERNAME}/smartrecipe-frontend:${IMAGE_TAG}
    build: ~
```

בסביבת ייצור, תמונות מורדות מ-Docker Hub. לא בונים locally.

---

## 16. תהליך ה-CI/CD

### GitHub Actions — הטריגר

על כל `git push` לענף `main` מופעל ה-Workflow אוטומטית. הגדרה ב-`.github/workflows/ci-cd.yml`.

### שלבי הפייפליין

**שלב 1 — Test:**

מופעל container של MySQL 8.0 כשירות בתוך ה-Runner. הבדיקות מתחברות ל-MySQL **אמיתי** (לא mock):

```yaml
services:
  mysql:
    image: mysql:8.0
    ports: ["3307:3306"]
    options: --health-cmd="mysqladmin ping..."
```

הרצת pytest עם כיסוי קוד:
```bash
pytest --cov=app --cov-report=xml -v
```

**במידה והבדיקות נכשלות** — הפייפליין נעצר ומייל נשלח:

```yaml
- name: Send failure email
  if: failure()
  uses: dawidd6/action-send-mail@v3
  with:
    subject: "❌ CI FAILED — Tests failed on commit ${{ github.sha }}"
    body: |
      Pipeline failed at: Test stage
      View: https://github.com/.../actions/runs/${{ github.run_id }}
```

**שלב 2 — Build & Push:**

```yaml
- uses: docker/build-push-action@v5
  with:
    context: ./backend
    push: true
    tags: |
      username/smartrecipe-backend:latest
      username/smartrecipe-backend:sha-abc1234
    cache-from: type=gha      # ← cache בין ריצות
    cache-to: type=gha,mode=max
```

**Tag Strategy:**
- `:latest` — תמיד מצביע על הגרסה האחרונה
- `:sha-<hash>` — tag קבוע לכל commit, מאפשר Rollback מדויק

**שלב 3 — Deploy:**

```yaml
- uses: appleboy/ssh-action@v1.0.3
  with:
    host: ${{ secrets.HETZNER_HOST }}
    key: ${{ secrets.HETZNER_SSH_KEY }}
    script: |
      export IMAGE_TAG=sha-${{ github.sha }}
      bash /opt/smartrecipe/infrastructure/deploy.sh
```

ה-`deploy.sh` מריץ על השרת:
```bash
docker compose pull           # משיכת images חדשים
flask db upgrade              # migration של DB אם יש
docker compose up -d          # restart שירותים
docker image prune -f         # ניקוי ישנים
```

**שליחת מייל הצלחה בסיום פריסה מוצלחת.**

### פירוט שלבי הפייפליין

| שלב | תיאור | כישלון → |
|---|---|---|
| 1. Checkout | העתקת קבצי המקור ל-Runner | Pipeline נעצר |
| 2. Python Setup | התקנת Python + pip cache | Pipeline נעצר |
| 3. pip install | התקנת כל ה-dependencies | Pipeline נעצר |
| 4. pytest | הרצת 14 בדיקות מול MySQL | **Pipeline נעצר + מייל** |
| 5. Docker login | כניסה ל-Docker Hub | Pipeline נעצר |
| 6. Build backend | בניית Flask image | **Pipeline נעצר + מייל** |
| 7. Build frontend | בניית Nginx image | **Pipeline נעצר + מייל** |
| 8. SCP | העתקת קבצים לשרת | **Pipeline נעצר + מייל** |
| 9. SSH Deploy | הרצת deploy.sh בשרת | **Pipeline נעצר + מייל** |
| 10. Success mail | אישור פריסה מוצלחת | — |

---

## 17. עקרונות Git ו-CI/CD בפרויקט

### Git כמקור האמת לקוד ולקונפיגורציה

הפרויקט מיישם עקרונות GitOps ברמת הקוד והקונפיגורציה: **כל שינוי עובר דרך Git ומפעיל את הפייפליין האוטומטי**. חשוב לציין שהמונח "GitOps מלא" בתעשייה מתייחס בדרך כלל למערכות המבוססות Kubernetes עם כלי Reconciliation כמו ArgoCD או Flux — שם Kubernetes עצמו מסנכרן את מצב הייצור עם מה שמוגדר ב-Git באופן רציף. בפרויקט זה השתמשנו ב-GitHub Actions עם Docker Compose ו-SSH Deploy — שהוא CI/CD קלאסי שמיישם את עקרון "Git כמקור האמת" ברמת הקוד.

```
Git (main branch)
      │  כל push מפעיל את הפייפליין
      ▼
GitHub Actions
      │  Tests pass → Build → Push → Deploy
      ▼
Hetzner Server
      │  docker compose pull → up -d
      ▼
אפליקציה מעודכנת פעילה
```

**עקרונות שיושמו בפרויקט:**

1. **הכל ב-Git** — קוד, Dockerfiles, docker-compose, nginx.conf, scripts הכנת שרת
2. **אין שינויים ידניים בשרת** — כל שינוי עובר דרך הפייפליין בלבד
3. **Immutable Images** — כל deploy משתמש ב-image חדש עם sha tag ייחודי
4. **Rollback פשוט** — שינוי `IMAGE_TAG` ל-sha קודם ו-push → הפייפליין פורס את הגרסה הישנה

---

## 18. תשתית הענן — Hetzner

### הכנת השרת — hetzner_setup.sh

סקריפט Bash שמכין שרת Ubuntu 22.04 מאפס:

```bash
# 1. עדכון packages
apt-get update && apt-get upgrade -y

# 2. התקנת Docker מה-repository הרשמי
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor...
apt-get install docker-ce docker-ce-cli containerd.io

# 3. יצירת deploy user עם הרשאות Docker
useradd -m -s /bin/bash deploy
usermod -aG docker deploy

# 4. קונפיגורציית Firewall (UFW — Security Groups)
ufw allow 80/tcp    # אפליקציה
ufw allow 443/tcp   # HTTPS
ufw allow ssh       # ניהול
ufw allow 3000/tcp  # Grafana
ufw allow 9090/tcp  # Prometheus

# 5. יצירת ספריות לנתונים קבועים
mkdir -p /opt/smartrecipe/{mysql_data,prometheus_data,grafana_data}
```

### Firewall — Security Groups

בדומה ל-Security Groups ב-AWS, UFW (Uncomplicated Firewall) בלינוקס מגדיר אילו פורטים פתוחים. רק פורטים הכרחיים פתוחים — MySQL (3306) **סגור** לחלוטין לעולם החיצוני.

### deploy.sh — אוטומציית הפריסה

הסקריפט שרץ בשרת על כל Deployment:

```bash
cd /opt/smartrecipe
docker compose -f docker-compose.yml -f docker-compose.prod.yml pull
docker compose -f docker-compose.yml -f docker-compose.prod.yml run \
  --rm backend flask db upgrade
docker compose -f docker-compose.yml -f docker-compose.prod.yml \
  up -d --remove-orphans
docker image prune -f
```

---

## 19. ניטור

### Prometheus — איסוף מדדים

Prometheus מתחבר כל 15 שניות ל-`/metrics` של Flask (דרך `prometheus-flask-exporter`) ושומר נתונים:

```yaml
scrape_configs:
  - job_name: "smartrecipe-backend"
    static_configs:
      - targets: ["backend:5000"]
    metrics_path: "/metrics"
```

**מדדים אוטומטיים לכל endpoint:**

| מדד | תיאור |
|---|---|
| `flask_http_request_total` | סך הבקשות לפי method, path, status |
| `flask_http_request_duration_seconds` | זמני תגובה (histogram) |
| `flask_http_request_exceptions_total` | בקשות שגרמו ל-exception |

### Grafana — ויזואליזציה

Dashboard מוכן מראש (Provisioning — Configuration as Code):

```yaml
# datasources/prometheus.yml
datasources:
  - name: Prometheus
    type: prometheus
    url: http://prometheus:9090
    isDefault: true
```

**הגרפים ב-Dashboard:**
- HTTP Request Rate — קצב בקשות לפי endpoint
- p95 Latency — זמן תגובה של אחוזון 95
- Total Requests — counter מצטבר
- 5xx Error Rate — שגיאות שרת לשנייה

הכל נטען אוטומטית בהרצת `docker compose up`. **אין הגדרה ידנית.**

### גישה לממשקי הניטור

פורטים 9090 (Prometheus) ו-3000 (Grafana) פתוחים כרגע לכל IP בשרת הייצור. בסביבת ייצור מאובטחת יש להגביל גישה אליהם לכתובות IP מורשות בלבד באמצעות UFW:

```bash
# דוגמה — גישה ל-Grafana ו-Prometheus רק מ-IP ספציפי
ufw allow from 1.2.3.4 to any port 3000
ufw allow from 1.2.3.4 to any port 9090
ufw delete allow 3000/tcp
ufw delete allow 9090/tcp
```

---

## 20. אבטחת הפייפליין — Secrets

### GitHub Secrets

כל הפריטים הרגישים מאוחסנים ב-GitHub Secrets:

| Secret | שימוש |
|---|---|
| `DOCKER_HUB_USERNAME` | שם משתמש Docker Hub |
| `DOCKER_HUB_TOKEN` | Access Token (לא סיסמה) |
| `HETZNER_HOST` | IP השרת |
| `HETZNER_USER` | משתמש SSH |
| `HETZNER_SSH_KEY` | מפתח SSH פרטי |
| `GEMINI_API_KEY` | מפתח Gemini AI |
| `MAIL_USERNAME` | מייל לשליחת התראות |
| `MAIL_PASSWORD` | App Password של Gmail |
| `MAIL_RECIPIENT` | כתובת לקבלת התראות |

### Docker Secrets / Environment Variables

```yaml
# docker-compose.yml — המשתנים מגיעים מ-.env
environment:
  GEMINI_API_KEY: ${GEMINI_API_KEY}
  MYSQL_PASSWORD: ${MYSQL_PASSWORD}
  SECRET_KEY: ${SECRET_KEY}
```

קובץ `.env` נמצא ב-`.gitignore` ולא מועלה לGit.

### עקרונות אבטחה נוספים

1. **MySQL לא חשוף לאינטרנט** — רק ברשת Docker הפנימית
2. **Flask לא חשוף לאינטרנט** — רק Nginx
3. **HTTPS** — כרגע האתר פועל על HTTP בלבד. בסביבת ייצור ניתן להוסיף Let's Encrypt באמצעות Certbot ל-Nginx ללא שינוי בקוד האפליקציה
4. **SQLAlchemy ORM** — הגנה מובנית מ-SQL Injection
5. **Security Headers** — X-Frame-Options, X-XSS-Protection ב-Nginx

---

## 21. בדיקות — pytest

### אסטרטגיית הבדיקות

הבדיקות מחולקות לשתי קטגוריות, ושתיהן רצות מול **MySQL אמיתי** (לא mock) — כפי שנדרש באפיון:

> "טסט שבודק הכנסה/הוצאה מה-DB ועובר כמובן דרך השרת"

### test_db.py — בדיקות הכנסה/הוצאה מה-DB

| בדיקה | מה נבדק |
|---|---|
| `test_insert_recipe` | הכנסת רשומה ל-DB ווידוא קבלת ID |
| `test_retrieve_recipe` | שמירה ושליפה לפי שדה |
| `test_update_recipe` | עדכון שדה ווידוא הנתונים החדשים |
| `test_delete_recipe` | מחיקה ווידוא שהרשומה נמחקה |
| `test_recipe_to_dict` | serialization לפורמט JSON |

### test_api.py — בדיקות API דרך השרת

| בדיקה | מה נבדק |
|---|---|
| `test_health_endpoint` | GET /health מחזיר 200 |
| `test_list_recipes_empty` | GET /api/recipes מחזיר JSON תקין |
| `test_save_recipe` | POST יוצר רשומה ומחזיר 201 |
| `test_get_recipe` | GET /:id מחזיר את הרשומה הנכונה |
| `test_update_recipe` | PUT מעדכן שדה |
| `test_delete_recipe` | DELETE מוחק ומחזיר 404 לאחר מכן |
| `test_save_recipe_missing_field` | POST ללא שדה חובה → 400 |
| `test_generate_recipe_missing_ingredients` | POST ללא מרכיבים → 400 |

### conftest.py — Fixtures

```python
@pytest.fixture(scope="session")
def app():
    application = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": TEST_DB_URL,
    })
    with application.app_context():
        db.create_all()      # יצירת טבלאות לפני הסשן
        yield application
        db.drop_all()        # ניקוי בסיום
```

`scope="session"` — ה-DB נוצר פעם אחת לכל ריצת pytest, לא לכל בדיקה. מהיר יותר.

### הרצת הבדיקות ב-CI

```yaml
# GitHub Actions — MySQL אמיתי כ-service
services:
  mysql:
    image: mysql:8.0
    ports: ["3307:3306"]

- name: Run tests
  env:
    TEST_DATABASE_URL: mysql+pymysql://...@127.0.0.1:3307/smartrecipe_test
  run: pytest --cov=app --cov-report=xml -v
```

---

## 22. שאלות צפויות מהבוחן

| שאלה | תשובה |
|---|---|
| **למה Hetzner ולא AWS?** | Hetzner מציע VPS זול יותר משמעותית (2-5€/חודש לעומת עשרות דולרים ב-AWS EC2). לפרויקט בסדר גודל זה, עם Docker Compose ואפליקציה אחת, אין צורך בשירותים המנוהלים של AWS. כל יכולות ה-DevOps (Docker, SSH, firewall) זמינות בשרת Ubuntu רגיל. |
| **למה Docker Compose ולא Kubernetes?** | Kubernetes מתאים למערכות עם עשרות מיקרו-שירותים שצריכים auto-scaling, self-healing, ו-rolling updates מתקדמים. לפרויקט זה עם 5 שירותים, Docker Compose פשוט יותר לתפעול, קל יותר לדיבאג, ומספיק לגמרי. Kubernetes היה מוסיף מורכבות ללא ערך מוסף. |
| **למה Flask ולא FastAPI?** | Flask הוא הפריימוורק הנפוץ ביותר בקורסי Python ומוכר יותר לבוחנים. FastAPI מהיר יותר ותומך ב-async, אך Flask מספיק לאפליקציה זו ויש לו ecosystem עשיר יותר (Flask-SQLAlchemy, Flask-Migrate). |
| **למה MySQL ולא PostgreSQL?** | MySQL מוכר יותר בקורסים ובתעשייה לפרויקטים בסדר גודל זה. לשניהם ביצועים דומים לאפליקציה כזו. אם היה צורך ב-JSON columns מתקדמים או Full-Text Search מורכב, PostgreSQL היה עדיף. |
| **למה GitHub Actions ולא Jenkins?** | GitHub Actions משולב ישירות בגיטהאב — אין צורך בשרת Jenkins נפרד. עבור פרויקט בודד, Jenkins מוסיף תשתית לתחזוקה ללא יתרון. GitHub Actions חינמי לפרויקטים פתוחים ומספיק בעוצמתו. |
| **איך מתבצע Rollback?** | לכל commit יש Docker image עם tag `:sha-<hash>` ייחודי. לחזרה לגרסה קודמת: משנים את `IMAGE_TAG` ב-`.env` בשרת לשה הרצויה, ומריצים `docker compose up -d`. אפשר גם לבצע `git revert` ו-push — הפייפליין יפרוס את הגרסה הישנה אוטומטית. |
| **איך נשמרים הסודות?** | שלוש שכבות: (1) ב-GitHub Secrets לפייפליין — מוצפנים ולא נחשפים ב-logs. (2) ב-`.env` בשרת הייצור — לא ב-Git, הרשאות 600. (3) בקוד — רק דרך `os.getenv()`, לא hard-coded. |
| **מה קורה אם Gemini לא זמין?** | הבקשה נכשלת עם HTTP 500 ומוחזרת הודעת שגיאה ידידותית. השגיאה נרשמת ב-logs. האפליקציה ממשיכה לעבוד לגמרי — כל הפיצ'רים של CRUD מתכונים (שמירה, צפייה, עדכון, מחיקה) אינם תלויים ב-Gemini. |
| **איך הבדיקות מתחברות למסד הנתונים?** | ב-CI, GitHub Actions מרים container של MySQL כ-service במכונה הזמנית. הבדיקות מתחברות ל-`127.0.0.1:3307` — MySQL אמיתי, לא mock. ה-connection string מועבר כ-environment variable `TEST_DATABASE_URL`. |
| **מה ההבדל בין Docker Volume לבין Backup?** | Volume מגן מפני מחיקת נתונים כשה-container נעצר. אבל אם הדיסק ניזוק, Volume נמחק, או docker compose down -v מורץ — הנתונים אבודים. גיבוי (mysqldump יומי) שומר עותק של הנתונים במקום חיצוני ומאפשר שחזור. אחד לא מחליף את השני. |

---

## 23. סיכום

### מה הושג בפרויקט

הפרויקט מימש את כל דרישות האפיון:

| דרישה מהאפיון | מה בוצע | סטטוס |
|---|---|---|
| Flask backend | Flask 3.0 + Gunicorn, REST API מלא | ✅ |
| Nginx — Load Balancing / File Server | nginx.conf עם upstream + static files | ✅ |
| MySQL + חיבורי API | SQLAlchemy ORM + Flask-Migrate | ✅ |
| אריזה בדוקר (שרת, DB, Nginx) | 5 containers ב-Docker Compose | ✅ |
| אחסון פריטים רגישים (Secrets) | GitHub Secrets + .env + .gitignore | ✅ |
| pytest — בדיקת הכנסה/הוצאה מה-DB | 14 בדיקות מול MySQL אמיתי | ✅ |
| CI — הרצה בעדכון קוד | GitHub Actions trigger on push | ✅ |
| עדכון מייל אם נכשל | dawidd6/action-send-mail@v3 | ✅ |
| העברת images ל-Docker Hub | Build & Push עם :latest + :sha | ✅ |
| פריסה בענן (Hetzner במקום EC2) | SSH deploy + docker compose up | ✅ |
| Bash script בהרצת המכונה | hetzner_setup.sh + deploy.sh | ✅ |
| Prometheus + Grafana | containers + provisioning מוכן | ✅ |
| AI integration | Gemini 1.5 Flash במקום OpenAI | ✅ |

### לקחים עיקריים

1. **CI/CD אוטומטי עובד** — כל שינוי עובר דרך Git → pipeline → ייצור. אין שינויים ידניים.
2. **Real DB בבדיקות** — בדיקות שמתחברות ל-MySQL אמיתי תופסות בעיות שmock לא יתפוס.
3. **Environment Variables חיוניים** — אף סוד לא מוטמע בקוד. ניתן להחליף בכל סביבה.
4. **Healthchecks מונעים בעיות** — ללא healthcheck, Flask יעלה לפני ש-MySQL מוכן ויקרוס.
5. **Monitoring מהיום הראשון** — קל יותר לבנות ניטור בתחילת פרויקט מאשר להוסיפו בהמשך.
6. **Docker cache** — סדר הפקודות ב-Dockerfile משפיע ישירות על זמן הבנייה.

### כיוונים עתידיים

- **HTTPS** — הוספת Let's Encrypt/Certbot ל-Nginx
- **Kubernetes** — מעבר מ-Docker Compose ל-k8s לסקיילינג
- **Terraform** — הגדרת תשתית Hetzner כקוד (IaC)
- **Redis** — Cache לתוצאות Gemini שנוצרו לאחרונה
- **Rate Limiting** — הגבלת קריאות ל-Gemini API לפי משתמש
- **JWT Authentication** — ניהול משתמשים עם JWT tokens

---

*ספר פרויקט זה נכתב כחלק מפרויקט הסיום בקורס DevOps Engineering.*
*הקוד המלא זמין ב-GitHub: https://github.com/gad-rapaport/devops-final-project*
