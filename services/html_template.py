"""
Reusable HTML template for AI Daily News.
"""


def get_html_template() -> str:
    """
    Returns the base HTML template.

    The placeholders will be replaced by the
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

        body{

            margin:0;

            padding:0;

            background:#f4f6fb;

            font-family:Arial,Helvetica,sans-serif;

        }

        .container{

            max-width:900px;

            margin:40px auto;

            background:white;

            border-radius:14px;

            overflow:hidden;

            box-shadow:0 6px 20px rgba(0,0,0,.08);

        }

        .header{

            background:#111827;

            color:white;

            padding:40px;

        }

        .header h1{

            margin:0;

            font-size:34px;

        }

        .header p{

            opacity:.85;

        }

        .section{

            padding:35px;

        }

        .section-title{

            color:#2563eb;

            border-bottom:2px solid #2563eb;

            padding-bottom:8px;

            margin-bottom:25px;

        }

        .article{

            border:1px solid #e5e7eb;

            border-radius:12px;

            padding:22px;

            margin-bottom:22px;

        }

        .article h3{

            margin-top:0;

        }

        .meta{

            color:#6b7280;

            font-size:14px;

        }

        .summary{

            margin-top:15px;

            line-height:1.7;

        }

        .button{

            display:inline-block;

            margin-top:18px;

            padding:10px 20px;

            background:#2563eb;

            color:white;

            text-decoration:none;

            border-radius:8px;

        }

        .footer{

            background:#111827;

            color:white;

            text-align:center;

            padding:25px;

            font-size:14px;

        }

        </style>

        </head>

        <body>

        <div class="container">

        <div class="header">

        <h1>🤖 {{TITLE}}</h1>

        <p>{{DATE}}</p>

        </div>

        {{CONTENT}}

        <div class="footer">

        Generated automatically by AI Daily News Agent - Jay Karkar

        </div>

        </div>

        </body>

        </html>
        """