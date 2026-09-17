import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#475569"))
        
        # Cover page has no header/footer
        if self._pageNumber > 1:
            # Running header
            self.drawString(54, 11 * 72 - 36, "QUICKTASK — AI-Powered Task & Productivity Platform")
            self.setFont("Helvetica", 8)
            self.drawRightString(8.5 * 72 - 54, 11 * 72 - 36, "System Architecture & Engineering Manual")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.75)
            self.line(54, 11 * 72 - 42, 8.5 * 72 - 54, 11 * 72 - 42)
            
            # Running footer
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.75)
            self.line(54, 46, 8.5 * 72 - 54, 46)
            self.drawString(54, 32, "Enterprise Architecture Documentation — Project Completed & Verified")
            page_text = f"Page {self._pageNumber} of {page_count}"
            self.drawRightString(8.5 * 72 - 54, 32, page_text)
            
        self.restoreState()

def build_pdf(filename="docs/QuickTask_Complete_Documentation.pdf"):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=50,
        rightMargin=50,
        topMargin=50,
        bottomMargin=50
    )
    
    styles = getSampleStyleSheet()
    
    # Elegant Color Palette
    PRIMARY = colors.HexColor("#0F172A")    # Deep Slate
    SECONDARY = colors.HexColor("#4338CA")  # Indigo
    ACCENT = colors.HexColor("#2563EB")     # Blue
    TEXT_DARK = colors.HexColor("#1E293B")  # Charcoal
    TEXT_MUTED = colors.HexColor("#64748B") # Slate Gray
    BG_LIGHT = colors.HexColor("#F8FAFC")   # Soft Off-white
    BORDER_COLOR = colors.HexColor("#E2E8F0")
    GREEN_ACCENT = colors.HexColor("#059669")
    CARD_BG = colors.HexColor("#F1F5F9")
    
    # Typography Styles
    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=30,
        textColor=PRIMARY,
        spaceAfter=6
    )
    
    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=SECONDARY,
        spaceAfter=12
    )
    
    meta_style = ParagraphStyle(
        'CoverMeta',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=13,
        textColor=TEXT_DARK
    )
    
    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=PRIMARY,
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )
    
    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=SECONDARY,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13.5,
        textColor=TEXT_DARK,
        spaceAfter=5
    )
    
    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=body_style,
        leftIndent=14,
        firstLineIndent=-10,
        spaceAfter=3
    )
    
    code_style = ParagraphStyle(
        'Code_Custom',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=7.8,
        leading=10.5,
        textColor=colors.HexColor("#0F172A")
    )
    
    callout_style = ParagraphStyle(
        'CalloutText',
        parent=body_style,
        fontSize=8.5,
        leading=12.5,
        textColor=colors.HexColor("#1E293B")
    )
    
    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=TEXT_DARK
    )
    
    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=11,
        textColor=colors.white
    )

    story = []
    
    def add_callout(text, bg_color=BG_LIGHT, border_color=SECONDARY):
        p = Paragraph(text, callout_style)
        t = Table([[p]], colWidths=[512])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), bg_color),
            ('BOX', (0,0), (-1,-1), 1, border_color),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ]))
        story.append(t)
        story.append(Spacer(1, 6))

    # ==========================================
    # HEADER & HERO BANNER
    # ==========================================
    story.append(Paragraph("ENTERPRISE PLATFORM SPECIFICATION", subtitle_style))
    story.append(Paragraph("QuickTask: AI-Powered Employee Task &amp; Productivity Platform", title_style))
    story.append(Paragraph("Complete Technical Architecture, Workflows, Functional Modules, Directory Structure &amp; Operations Manual", ParagraphStyle('SubDesc', parent=body_style, fontSize=10, leading=14, textColor=TEXT_MUTED)))
    story.append(Spacer(1, 8))
    story.append(HRFlowable(width="100%", thickness=1.5, color=SECONDARY, spaceAfter=10))
    
    meta_table_data = [
        [Paragraph("<b>Project:</b> QuickTask Full-Stack", meta_style), 
         Paragraph("<b>Repository:</b> github.com/MEHTHAB7/QUICK_TASK", meta_style),
         Paragraph("<b>Live Deployment:</b> mehthab7.github.io/QUICK_TASK", meta_style)],
        [Paragraph("<b>Author:</b> MEHTHAB7", meta_style), 
         Paragraph("<b>Version:</b> 1.0.0 (Production Verified)", meta_style),
         Paragraph("<b>Stack:</b> React 19, FastAPI, Scikit-Learn, SQLite/Postgres", meta_style)],
    ]
    meta_table = Table(meta_table_data, colWidths=[160, 185, 167])
    meta_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 10))

    # ==========================================
    # 1. WHY USE THIS PLATFORM? (PROBLEM & SOLUTION)
    # ==========================================
    story.append(Paragraph("1. Purpose &amp; Value Proposition — Why Use QuickTask?", h1_style))
    story.append(Paragraph(
        "Modern companies face high friction managing dispersed workforces across isolated applications: one tool for task assignment (Trello/Jira), "
        "another for daily attendance (HR portals), third-party chat (Slack), and manual spreadsheets for retrospective productivity calculations. "
        "This fragmentation results in delayed bottleneck identification, employee burnout, and administrative overhead. "
        "<b>QuickTask resolves this by consolidating all four pillars into a unified, AI-driven platform.</b>",
        body_style
    ))
    
    add_callout(
        "<b>Core Innovation:</b> Rather than reviewing missed deadlines weeks after they occur, QuickTask's built-in <b>Scikit-Learn Machine Learning Engine</b> "
        "actively computes employee productivity and efficiency trajectories in real-time, surfacing proactive <i>At-Risk Alerts</i> so managers can intervene before deadlines slip.",
        BG_LIGHT, SECONDARY
    )
    
    story.append(Paragraph("Key Strategic Advantages:", h2_style))
    story.append(Paragraph("• <b>Unified Operational Visibility:</b> Centralizes task management, attendance check-ins/outs, team messaging, and analytics into one coherent dashboard.", bullet_style))
    story.append(Paragraph("• <b>Objective, Data-Driven Performance Scoring:</b> Removes subjective bias by calculating normalized (0–100) productivity metrics based on completion ratio, workload velocity, and attendance consistency.", bullet_style))
    story.append(Paragraph("• <b>Real-Time Instant Collaboration:</b> Native WebSocket duplex communication enables synchronous team discussions without external third-party chat subscriptions.", bullet_style))
    story.append(Paragraph("• <b>Automated PDF Audit Generation:</b> Executive summaries and productivity reports are compiled programmatically into vector PDF documents with zero external dependencies.", bullet_style))
    story.append(Paragraph("• <b>Multi-Environment Ready:</b> Seamless transition from lightweight local SQLite development to high-concurrency Docker Compose (Postgres + Redis) and cloud hosting.", bullet_style))
    story.append(Spacer(1, 8))

    # ==========================================
    # 2. SYSTEM ARCHITECTURE & TECH STACK
    # ==========================================
    story.append(Paragraph("2. System Architecture &amp; Technology Stack", h1_style))
    story.append(Paragraph(
        "QuickTask is architected as an asynchronous, layered <b>Client-Server Application</b>. The frontend and backend communicate exclusively "
        "via authenticated JSON REST APIs and bi-directional WebSocket channels, enabling high concurrency and clean separation of concerns.",
        body_style
    ))
    
    tech_data = [
        [Paragraph("Layer", table_header_style), Paragraph("Technology", table_header_style), Paragraph("Architectural Rationale &amp; Key Responsibilities", table_header_style)],
        [Paragraph("<b>Frontend SPA</b>", table_cell_style), 
         Paragraph("React 19, Tailwind CSS v4, Framer Motion, Recharts, Vite 8", table_cell_style),
         Paragraph("High-performance responsive single-page application, 60fps animations, interactive SVG charts, client-side routing with GitHub Pages compatibility.", table_cell_style)],
        [Paragraph("<b>Backend API</b>", table_cell_style), 
         Paragraph("Python 3.11/3.13, FastAPI, Starlette, Uvicorn, Pydantic v2", table_cell_style),
         Paragraph("Asynchronous ASGI request pipeline, high throughput, automatic OpenAPI documentation, strict request/response data contracts.", table_cell_style)],
        [Paragraph("<b>Security &amp; Auth</b>", table_cell_style), 
         Paragraph("PyJWT, Bcrypt, Role-Based Access Control (RBAC)", table_cell_style),
         Paragraph("Stateless Bearer token validation, cryptographic password salting and hashing, role authorization guards (Admin, Manager, Employee).", table_cell_style)],
        [Paragraph("<b>Database &amp; ORM</b>", table_cell_style), 
         Paragraph("SQLAlchemy 2.0, Alembic, SQLite (Dev), PostgreSQL (Prod)", table_cell_style),
         Paragraph("Enterprise relational data modeling, automated schema migrations, zero-config local SQLite file persistence, pooled production queries.", table_cell_style)],
        [Paragraph("<b>AI / ML Engine</b>", table_cell_style), 
         Paragraph("Scikit-Learn, Pandas, NumPy, Joblib", table_cell_style),
         Paragraph("Pre-trained regression model inferring productivity scores from task completion ratio, impending deadlines, and attendance hours.", table_cell_style)],
        [Paragraph("<b>Real-Time &amp; Docs</b>", table_cell_style), 
         Paragraph("Starlette WebSockets, ReportLab PDF Engine", table_cell_style),
         Paragraph("Duplex broadcasting for team messaging; programmatic vector PDF generation for executive audit summaries.", table_cell_style)],
    ]
    t_tech = Table(tech_data, colWidths=[85, 145, 282])
    t_tech.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, BG_LIGHT]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_tech)
    story.append(Spacer(1, 10))

    # ==========================================
    # 3. DIRECTORY & CODEBASE STRUCTURE
    # ==========================================
    story.append(Paragraph("3. Directory &amp; Codebase Structure", h1_style))
    story.append(Paragraph("The repository is cleanly partitioned into modular frontend, backend, and deployment directories:", body_style))
    
    code_tree = """Quick_task/
|-- .github/workflows/deploy.yml   # GitHub Actions CI/CD to build & deploy frontend to GitHub Pages
|-- .gitignore                     # Root exclusion filter (venv, node_modules, dist, temp caches)
|-- docker-compose.yml             # Orchestration for PostgreSQL, Redis, FastAPI Backend, Frontend
|-- README.md                      # Complete installation, setup, credentials, and API docs
|-- generate_docs_pdf.py           # Programmatic ReportLab PDF documentation compiler
|-- docs/
|   +-- QuickTask_Complete_Documentation.pdf # Complete system architecture manual (this PDF)
|-- backend/
|   |-- alembic/                   # Database version scripts (migrations)
|   |-- app/
|   |   |-- api/                   # REST API routes and dependency injection (deps.py)
|   |   |   +-- endpoints/         # auth, users, tasks, attendance, analytics, reports, websockets
|   |   |-- core/                  # App settings (config.py) and security hashing/JWT (security.py)
|   |   |-- crud/                  # Data access layer (crud_user, crud_task, crud_attendance)
|   |   |-- db/                    # SQLAlchemy engine, session maker, base declarative model
|   |   |-- models/                # Database entities: User, Task, Attendance, Message
|   |   +-- schemas/               # Pydantic validation models for input/output serialization
|   |-- ml_models/                 # Scikit-learn model binary (joblib) and training pipeline
|   |-- app.db                     # Development SQLite database pre-seeded with test accounts
|   +-- requirements.txt           # Python backend dependencies
+-- frontend/
    |-- public/                    # Static assets, SVG icons, 404 fallback routing for GitHub Pages
    |-- src/
    |   |-- components/            # UI library: Sidebar navigation, metric cards, modals
    |   |-- context/               # AuthContext: JWT bearer token state & user role management
    |   |-- layouts/               # ProtectedLayout: standard dashboard framing and navigation
    |   |-- pages/                 # Views: Dashboard, TaskBoard, AttendanceLog, Analytics, Chat, Login
    |   |-- services/              # Axios HTTP client with auto-injecting JWT authorization header
    |   |-- App.jsx & main.jsx     # Client-side router configuration with base path awareness
    +-- vite.config.js             # Vite bundler configuration with Tailwind CSS v4 integration"""
    
    tree_p = Paragraph(code_tree.replace(" ", "&nbsp;").replace("\n", "<br/>"), code_style)
    tree_table = Table([[tree_p]], colWidths=[512])
    tree_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), CARD_BG),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(tree_table)
    story.append(Spacer(1, 10))

    # ==========================================
    # 4. HOW IT WORKS: MODULES & USER WORKFLOWS
    # ==========================================
    story.append(Paragraph("4. How It Works — Core Functional Modules &amp; Workflows", h1_style))
    
    story.append(Paragraph("A. Role-Based Access Control &amp; Authentication Flow", h2_style))
    story.append(Paragraph(
        "Users authenticate at <code>/login</code> via <code>POST /api/v1/auth/login</code>. The backend verifies the password hash using Bcrypt "
        "and generates a signed JWT containing the user's ID, email, and role. The frontend stores this in <code>localStorage</code>, "
        "which is automatically attached to every subsequent outgoing request via Axios interceptors.",
        body_style
    ))
    story.append(Paragraph("• <b>Admin:</b> Global control. Manages all users, views aggregate company metrics, executes ML models, and downloads PDF reports.", bullet_style))
    story.append(Paragraph("• <b>Manager:</b> Departmental delegation. Assigns tasks to specific employees, monitors status boards, and reviews team attendance.", bullet_style))
    story.append(Paragraph("• <b>Employee:</b> Daily execution. Views assigned tasks on a personal board, updates progress, checks in/out, and chats with team members.", bullet_style))
    
    story.append(Paragraph("B. Task Lifecycle &amp; Kanban State Machine", h2_style))
    story.append(Paragraph(
        "Tasks progress deterministically through three states: <b>Pending → In Progress → Completed</b>. "
        "Each task records priority (Low, Medium, High, Critical), assigned employee ID, deadline, and detailed description. "
        "State changes trigger updates in the database and feed into the AI productivity evaluation.",
        body_style
    ))

    story.append(Paragraph("C. Attendance &amp; Working Hours Tracking", h2_style))
    story.append(Paragraph(
        "Employees record daily check-ins upon starting work and check-outs upon completion. The backend computes active working hours, "
        "stores historical timestamps in the <code>attendance</code> table, and validates continuity. This prevents absentee logging and supplies "
        "critical attendance regularity metrics to the ML engine.",
        body_style
    ))

    story.append(Paragraph("D. AI Productivity Prediction &amp; At-Risk Detection", h2_style))
    story.append(Paragraph(
        "The machine learning subsystem in <code>backend/ml_models/</code> utilizes a trained <b>Random Forest / Linear Regression Model</b>. "
        "It evaluates three core feature vectors:",
        body_style
    ))
    story.append(Paragraph("1. <b>Velocity Ratio:</b> Ratio of completed tasks to total assigned tasks over a rolling 30-day window.", bullet_style))
    story.append(Paragraph("2. <b>Deadline Pressure:</b> Number of active tasks within 48 hours of expiration or overdue.", bullet_style))
    story.append(Paragraph("3. <b>Attendance Factor:</b> Cumulative logged hours versus scheduled working hours.", bullet_style))
    story.append(Paragraph(
        "The endpoint <code>POST /api/v1/analytics/predict-productivity</code> outputs a calibrated score from 0 to 100. "
        "Employees scoring below 60 are automatically highlighted on the Admin dashboard with an <i>At-Risk Warning</i>, "
        "allowing managers to reassign tasks or assist the employee before performance deteriorates.",
        body_style
    ))

    story.append(Paragraph("E. Real-Time Team Communication (WebSockets)", h2_style))
    story.append(Paragraph(
        "FastAPI's native WebSocket handler at <code>/api/v1/ws/chat</code> maintains open duplex channels with connected clients. "
        "Messages are parsed, augmented with user metadata and server timestamps, and broadcast to all active subscribers. "
        "The frontend uses React refs and hooks with auto-reconnection to provide a smooth, low-latency chat experience.",
        body_style
    ))

    story.append(Paragraph("F. Automated Vector PDF Audit Reports", h2_style))
    story.append(Paragraph(
        "Admins can trigger on-demand executive summary reports via <code>GET /api/v1/reports/productivity-report</code>. "
        "The backend queries live database metrics, draws a clean vector layout in an in-memory byte stream using ReportLab, "
        "and streams it directly to the user's browser with an <code>attachment</code> disposition for instant download.",
        body_style
    ))
    story.append(Spacer(1, 8))

    # ==========================================
    # 5. REST API SPECIFICATION TABLE
    # ==========================================
    story.append(Paragraph("5. Complete REST API Specification", h1_style))
    story.append(Paragraph("The backend adheres to RESTful conventions. Interactive documentation is available at <code>/docs</code>:", body_style))
    
    api_data = [
        [Paragraph("HTTP Method", table_header_style), Paragraph("API Endpoint", table_header_style), Paragraph("Access Role", table_header_style), Paragraph("Operation &amp; Purpose", table_header_style)],
        [Paragraph("<b>POST</b>", table_cell_style), Paragraph("<code>/api/v1/auth/login</code>", table_cell_style), Paragraph("Public", table_cell_style), Paragraph("Authenticates credentials; returns Bearer JWT access token.", table_cell_style)],
        [Paragraph("<b>GET</b>", table_cell_style), Paragraph("<code>/api/v1/users/</code>", table_cell_style), Paragraph("Admin", table_cell_style), Paragraph("Lists all employees, managers, and administrative users.", table_cell_style)],
        [Paragraph("<b>POST</b>", table_cell_style), Paragraph("<code>/api/v1/users/</code>", table_cell_style), Paragraph("Admin", table_cell_style), Paragraph("Registers a new employee or manager with role assignment.", table_cell_style)],
        [Paragraph("<b>GET</b>", table_cell_style), Paragraph("<code>/api/v1/tasks/</code>", table_cell_style), Paragraph("All Roles", table_cell_style), Paragraph("Fetches tasks (filtered by user assignment or admin global view).", table_cell_style)],
        [Paragraph("<b>POST</b>", table_cell_style), Paragraph("<code>/api/v1/tasks/</code>", table_cell_style), Paragraph("Admin, Mgr", table_cell_style), Paragraph("Creates and assigns a task with title, priority, and deadline.", table_cell_style)],
        [Paragraph("<b>PUT</b>", table_cell_style), Paragraph("<code>/api/v1/tasks/{id}</code>", table_cell_style), Paragraph("All Roles", table_cell_style), Paragraph("Transitions task status (Pending, In Progress, Completed).", table_cell_style)],
        [Paragraph("<b>POST</b>", table_cell_style), Paragraph("<code>/api/v1/attendance/check-in</code>", table_cell_style), Paragraph("Employee", table_cell_style), Paragraph("Logs employee daily check-in timestamp.", table_cell_style)],
        [Paragraph("<b>POST</b>", table_cell_style), Paragraph("<code>/api/v1/attendance/check-out</code>", table_cell_style), Paragraph("Employee", table_cell_style), Paragraph("Logs employee check-out and computes daily working hours.", table_cell_style)],
        [Paragraph("<b>GET</b>", table_cell_style), Paragraph("<code>/api/v1/analytics/dashboard-stats</code>", table_cell_style), Paragraph("All Roles", table_cell_style), Paragraph("Calculates system-wide counts, completion rates, and KPI trends.", table_cell_style)],
        [Paragraph("<b>POST</b>", table_cell_style), Paragraph("<code>/api/v1/analytics/predict-productivity</code>", table_cell_style), Paragraph("Admin, Mgr", table_cell_style), Paragraph("Feeds employee feature vectors into Scikit-Learn model to predict score.", table_cell_style)],
        [Paragraph("<b>GET</b>", table_cell_style), Paragraph("<code>/api/v1/reports/productivity-report</code>", table_cell_style), Paragraph("Admin", table_cell_style), Paragraph("Generates and downloads on-demand executive summary PDF report.", table_cell_style)],
        [Paragraph("<b>WS</b>", table_cell_style), Paragraph("<code>/api/v1/ws/chat</code>", table_cell_style), Paragraph("Authenticated", table_cell_style), Paragraph("Bidirectional WebSocket stream for low-latency team messaging.", table_cell_style)],
    ]
    t_api = Table(api_data, colWidths=[65, 175, 62, 210])
    t_api.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, BG_LIGHT]),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_api)
    story.append(Spacer(1, 10))

    # ==========================================
    # 6. DEPLOYMENT & PRODUCTION OPERATIONS
    # ==========================================
    story.append(Paragraph("6. Deployment &amp; CI/CD Operations", h1_style))
    story.append(Paragraph(
        "QuickTask is engineered for high operational flexibility across three deployment targets:",
        body_style
    ))
    
    story.append(Paragraph("1. Local Development (Instant Start)", h2_style))
    story.append(Paragraph("• <b>Backend:</b> Run <code>uvicorn app.main:app --reload --host 127.0.0.1 --port 8000</code> inside <code>backend/</code>. Uses SQLite (<code>app.db</code>).", bullet_style))
    story.append(Paragraph("• <b>Frontend:</b> Run <code>npm run dev</code> inside <code>frontend/</code>. Accessible at <code>http://localhost:5173</code> with hot module reloading.", bullet_style))

    story.append(Paragraph("2. GitHub Pages &amp; GitHub Actions (Automated Cloud CI/CD)", h2_style))
    story.append(Paragraph("• <b>Workflow:</b> <code>.github/workflows/deploy.yml</code> triggers on pushes to <code>main</code>.", bullet_style))
    story.append(Paragraph("• <b>Build Process:</b> Node 20 environment compiles the Vite React application with production asset optimization and sets base path to <code>/QUICK_TASK/</code>.", bullet_style))
    story.append(Paragraph("• <b>SPA Routing Fallback:</b> Copies <code>index.html</code> to <code>404.html</code>, enabling deep-linking and browser reloads without 404 errors on GitHub Pages.", bullet_style))
    story.append(Paragraph("• <b>Live URL:</b> <b>https://mehthab7.github.io/QUICK_TASK/</b>", bullet_style))

    story.append(Paragraph("3. Full Containerized Multi-Service Deployment (Docker Compose)", h2_style))
    story.append(Paragraph("Executing <code>docker-compose up -d --build</code> spins up four coordinated containers:", bullet_style))
    story.append(Paragraph("• <b>frontend:</b> Nginx Alpine serving optimized production builds on port 80.", bullet_style))
    story.append(Paragraph("• <b>backend:</b> FastAPI Python 3.11 container exposed on port 8000.", bullet_style))
    story.append(Paragraph("• <b>database:</b> PostgreSQL container initialized on port 5432.", bullet_style))
    story.append(Paragraph("• <b>cache:</b> Redis in-memory cache for distributed state on port 6379.", bullet_style))
    story.append(Spacer(1, 10))

    # ==========================================
    # 7. SEEDED CREDENTIALS & AUDIT SUMMARY
    # ==========================================
    story.append(PageBreak())
    story.append(Paragraph("7. Pre-Seeded Reference Accounts &amp; Validation", h1_style))
    story.append(Paragraph("The database contains pre-configured test users across all permission tiers for immediate testing:", body_style))
    
    cred_data = [
        [Paragraph("Role", table_header_style), Paragraph("Email Address", table_header_style), Paragraph("Password", table_header_style), Paragraph("Access Level &amp; Capabilities", table_header_style)],
        [Paragraph("<b>Admin</b>", table_cell_style), Paragraph("<code>admin@example.com</code>", table_cell_style), Paragraph("<code>password123</code>", table_cell_style), Paragraph("Full administrative rights: user registration, company analytics, AI scoring, PDF export.", table_cell_style)],
        [Paragraph("<b>Manager</b>", table_cell_style), Paragraph("<code>manager@example.com</code>", table_cell_style), Paragraph("<code>password123</code>", table_cell_style), Paragraph("Managerial rights: task creation, employee assignment, team attendance log inspection.", table_cell_style)],
        [Paragraph("<b>Employee</b>", table_cell_style), Paragraph("<code>employee@example.com</code>", table_cell_style), Paragraph("<code>password123</code>", table_cell_style), Paragraph("Personal workspace: assigned tasks, drag-and-drop status update, daily check-in/out, team chat.", table_cell_style)],
        [Paragraph("<b>Employee</b>", table_cell_style), Paragraph("<code>mehthab@gmail.com</code>", table_cell_style), Paragraph("<code>12345678</code>", table_cell_style), Paragraph("Personal employee account: task management, time tracking, real-time collaboration.", table_cell_style)],
    ]
    t_cred = Table(cred_data, colWidths=[70, 145, 95, 202])
    t_cred.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, BG_LIGHT]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_cred)
    story.append(Spacer(1, 12))

    # Sign-off Callout
    add_callout(
        "<b>Project Verification Sign-Off:</b> QuickTask is fully implemented, locally verified, container-ready, and deployed to GitHub Actions. "
        "All subsystems (Authentication, Task Engine, Attendance, AI Productivity Analytics, WebSocket Chat, and PDF Reporting) have completed verification without regression.",
        colors.HexColor("#F0FDF4"), GREEN_ACCENT
    )
    
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated PDF documentation at: {filename}")

if __name__ == '__main__':
    output_path = "docs/QuickTask_Complete_Documentation.pdf"
    if len(sys.argv) > 1:
        output_path = sys.argv[1]
    build_pdf(output_path)
