from flask import render_template
from app.website import website_bp

@website_bp.get("/donate")
def donate():

    return render_template(
        "website/donate.html"
    )

