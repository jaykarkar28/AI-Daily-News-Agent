"""
Reusable HTML template for AI Daily News.
"""


def get_html_template() -> str:
    """
    Returns the base HTML template.

    The placeholders are replaced by the
    HTML Generator.
    """

    return """
    <!DOCTYPE html>

    <html lang="en">

    <head>

    <meta charset="UTF-8">

    <meta
        name="viewport"
        content="width=device-width, initial-scale=1.0"
    >

    <title>{{TITLE}}</title>

    <style>

    *{

        box-sizing:border-box;

    }

    html{

        scroll-behavior:smooth;

    }

    body{

        margin:0;

        padding:0;

        background:#f3f6fb;

        color:#111827;

        font-family:
            "Segoe UI",
            Inter,
            Arial,
            sans-serif;

    }

    /* ---------------------------- */
    /* Container */
    /* ---------------------------- */

    .container{

        max-width:1100px;

        margin:40px auto;

        background:#ffffff;

        border-radius:18px;

        overflow:hidden;

        box-shadow:
            0 12px 40px rgba(0,0,0,.08);

        animation:
            fadeIn .6s ease;

    }

    /* ---------------------------- */
    /* Header */
    /* ---------------------------- */

    .header{

        background:
            linear-gradient(
                135deg,
                #2563eb,
                #4f46e5
            );

        color:white;

        padding:55px;

        box-shadow:
            0 8px 30px rgba(0,0,0,.15);

    }

    .header h1{

        margin:0;

        font-size:40px;

        font-weight:700;

    }

    .subtitle{

        margin-top:14px;

        font-size:24px;

        font-weight:500;

        opacity:.95;

    }

    .description{

        margin-top:24px;

        max-width:760px;

        font-size:17px;

        line-height:1.8;

        opacity:.92;

    }

    .header-date{

        display:inline-block;

        margin-top:28px;

        padding:12px 22px;

        background:rgba(255,255,255,.18);

        border-radius:10px;

        font-size:16px;

        font-weight:600;

    }

    /* ---------------------------- */
    /* Dashboard */
    /* ---------------------------- */

    .stats{

        display:flex;

        justify-content:space-between;

        gap:20px;

        padding:35px;

        background:#ffffff;

        border-bottom:1px solid #e5e7eb;

    }

    .stat-card{

        flex:1;

        background:#f8fafc;

        border-radius:14px;

        padding:24px;

        text-align:center;

        box-shadow:
            0 2px 10px rgba(0,0,0,.05);

        transition:
            transform .25s ease,
            box-shadow .25s ease;

    }

    .stat-card:hover{

        transform:translateY(-4px);

        box-shadow:
            0 10px 25px rgba(37,99,235,.12);

    }

    .stat-title{

        color:#6b7280;

        font-size:14px;

        margin-bottom:10px;

    }

    .stat-value{

        color:#2563eb;

        font-size:28px;

        font-weight:700;

    }

    /* ---------------------------- */
    /* Sections */
    /* ---------------------------- */

    .section{

        padding:40px;

    }

    .section-title{

        color:#2563eb;

        font-size:28px;

        margin-bottom:30px;

        padding-left:15px;

        padding-bottom:10px;

        border-left:6px solid #2563eb;

        border-bottom:2px solid #dbeafe;

    }

    /* ---------------------------- */
    /* Articles */
    /* ---------------------------- */

    .article{

        background:#ffffff;

        border:1px solid #e5e7eb;

        border-radius:16px;

        padding:24px;

        margin-bottom:35px;

        transition:
            transform .25s ease,
            box-shadow .25s ease;

    }

    .article:hover{

        transform:translateY(-4px);

        box-shadow:
            0 12px 30px rgba(37,99,235,.12);

    }

    .article h3{

        margin-top:0;

        color:#111827;

        font-size:24px;

    }

    .meta{

        color:#6b7280;

        font-size:14px;

        margin-bottom:16px;

    }
    
    .badges{

        margin:15px 0;

    }

    .badge{

        display:inline-block;

        margin:4px;

        padding:8px 14px;

        border-radius:999px;

        background:#eef4ff;

        color:#2563eb;

        font-size:13px;

        font-weight:600;

        border:1px solid #dbeafe;

        max-width:100%;

        box-sizing:border-box;

        word-break:break-word;

    }

    .badge.source{

        background:#eff6ff;

    }

    .badge.category{

        background:#f5f3ff;

        color:#7c3aed;

    }

    .badge.date{

        background:#f0fdf4;

        color:#15803d;

    }

    .badge.score{

        background:#fff7ed;

        color:#ea580c;

    }

    .summary{

        font-size:16px;

        color:#374151;

        line-height:1.8;

    }

    /* ---------------------------- */
    /* Button */
    /* ---------------------------- */

    .button{

        display:inline-block;

        margin-top:20px;

        padding:12px 24px;

        background:#2563eb;

        color:white;

        text-decoration:none;

        border-radius:10px;

        font-weight:600;

        box-shadow:
            0 4px 12px rgba(37,99,235,.25);

        transition:
            background .2s ease,
            transform .2s ease;

    }
    
    .button:link,
    .button:visited{

        color:#ffffff !important;

        text-decoration:none !important;

    }

    .button:hover{

        background:#1d4ed8;

        transform:translateY(-2px);

    }

    /* ---------------------------- */
    /* Footer */
    /* ---------------------------- */

    .footer{

        background:#111827;

        color:white;

        padding:35px;

        text-align:center;

        font-size:14px;

        line-height:1.8;

    }

    /* ---------------------------- */
    /* Animation */
    /* ---------------------------- */

    @keyframes fadeIn{

        from{

            opacity:0;

            transform:translateY(20px);

        }

        to{

            opacity:1;

            transform:translateY(0);

        }

    }

    /* ---------------------------- */
    /* Mobile */
    /* ---------------------------- */

    @media(max-width:768px){
        
        .header-date{

            width:100%;

            text-align:center;

        }

        .button{

            width:100%;

            text-align:center;

        }

        .badge{

            display:inline-block !important;

            width:calc(50% - 12px) !important;

            box-sizing:border-box;

            margin:4px !important;

            text-align:center !important;

            white-space:normal !important;

            word-break:break-word !important;

        }
        
        .badges{
            text-align:center !important;
        }

        .container{

            max-width:980px;
            width:100%;
            margin:30px auto;

        }

        .header{

            padding:35px;

        }

        .header h1{

            font-size:32px;

        }

        .subtitle{

            font-size:20px;

        }

        .description{

            font-size:15px;

        }

        .stats{

            flex-direction:column;

        }

        .section{

            padding:24px;

        }

        .article{

            padding:18px;

        }

        .article h3{

            font-size:20px;

        }

    }

    </style>

    </head>

    <body>

    <div class="container">

    <div class="header">

    <h1>
    🤖 {{TITLE}}
    </h1>

    <h2 class="subtitle">
    Daily AI Intelligence Brief
    </h2>

    <p class="description">

    Stay updated with the latest breakthroughs in
    Artificial Intelligence, Large Language Models,
    Research, Open Source projects,
    and Industry News.

    </p>

    <div class="header-date">

    📅 {{DATE}}

    </div>

    </div>

    {{STATS}}

    {{CONTENT}}

    <div class="footer">

    <strong>🤖 AI Daily News Agent</strong>

    <br><br>

    Powered by <strong>LangGraph • Groq • Python</strong>

    <br><br>

    Generated automatically for your daily AI insights.

    <br><br>

    © 2026 Jay Karkar

    </div>

    </div>

    </body>

    </html>
    """