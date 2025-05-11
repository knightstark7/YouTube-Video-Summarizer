def generate_html(title, topics, video_id=None, thumbnail_url=None):
    """
    Generate HTML page for video summary.
    
    Args:
        title: str, video title
        topics: list of dict, each containing:
            - topic: str, the topic name
            - summary: str, summary of the topic
            - questions: list of dict, each with 'question' and 'answer' keys
        video_id: str, the YouTube video ID (optional)
        thumbnail_url: str, URL to the video thumbnail (optional)
    """
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title} - Summary</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 900px;
                margin: 0 auto;
                padding: 20px;
                background-color: #f8f9fa;
            }}
            header {{
                text-align: center;
                margin-bottom: 30px;
                padding-bottom: 20px;
                border-bottom: 2px solid #e9ecef;
            }}
            .video-container {{
                display: flex;
                flex-direction: column;
                align-items: center;
                margin-bottom: 20px;
                background-color: white;
                border-radius: 8px;
                padding: 20px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            .thumbnail {{
                width: 100%;
                max-width: 640px;
                border-radius: 8px;
                margin-bottom: 15px;
                box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            }}
            .video-info {{
                text-align: center;
                width: 100%;
            }}
            .watch-button {{
                display: inline-block;
                background-color: #ff0000;
                color: white;
                padding: 10px 20px;
                text-decoration: none;
                border-radius: 4px;
                margin-top: 10px;
                font-weight: bold;
                transition: background-color 0.3s;
            }}
            .watch-button:hover {{
                background-color: #cc0000;
            }}
            h1 {{
                color: #2c3e50;
                margin-bottom: 10px;
            }}
            .subtitle {{
                color: #6c757d;
                font-style: italic;
            }}
            h2 {{
                color: #3498db;
                margin-top: 30px;
                border-bottom: 1px solid #eee;
                padding-bottom: 5px;
            }}
            .topic {{
                background-color: white;
                border-radius: 8px;
                padding: 20px;
                margin-bottom: 25px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            .question {{
                background-color: #e8f4fc;
                border-left: 4px solid #3498db;
                padding: 10px 15px;
                margin: 15px 0;
                border-radius: 0 4px 4px 0;
            }}
            .answer {{
                background-color: #f8f9fa;
                border-left: 4px solid #2ecc71;
                padding: 10px 15px;
                margin: 15px 0 15px 20px;
                border-radius: 0 4px 4px 0;
            }}
            footer {{
                text-align: center;
                margin-top: 30px;
                padding-top: 20px;
                border-top: 1px solid #e9ecef;
                color: #6c757d;
                font-size: 0.9em;
            }}
            .topics-container {{
                margin-top: 30px;
            }}
        </style>
    </head>
    <body>
        <header>
            <h1>{title}</h1>
            <p class="subtitle">Video Summary</p>
        </header>
    """
    
    # Add video thumbnail and link if available
    if thumbnail_url and video_id:
        html += f"""
        <div class="video-container">
            <img src="{thumbnail_url}" alt="Video thumbnail" class="thumbnail" onerror="this.onerror=null; this.src='https://img.youtube.com/vi/{video_id}/hqdefault.jpg';">
            <div class="video-info">
                <a href="https://www.youtube.com/watch?v={video_id}" target="_blank" class="watch-button">Watch on YouTube</a>
            </div>
        </div>
        """
    
    # Add topics section
    html += '<div class="topics-container">'
    
    for topic in topics:
        html += f"""
        <div class="topic">
            <h2>{topic['topic']}</h2>
            <p>{topic['summary']}</p>
        """
        
        if 'questions' in topic and topic['questions']:
            for qa in topic['questions']:
                html += f"""
                <div class="question">
                    <strong>Q:</strong> {qa['question']}
                </div>
                <div class="answer">
                    <strong>A:</strong> {qa['answer']}
                </div>
                """
            
        html += "</div>"
    
    html += """
        </div>
        <footer>
            Generated by YouTube Video Summarizer
        </footer>
    </body>
    </html>
    """
    
    return html

def save_html(html_content, filename="video_summary.html"):
    """Save HTML content to a file."""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        return True
    except Exception as e:
        print(f"Error saving HTML: {e}")
        return False

if __name__ == "__main__":
    # Test HTML generation with sample data
    test_title = "Sample Video Title"
    test_video_id = "dQw4w9WgXcQ"
    test_thumbnail = f"https://img.youtube.com/vi/{test_video_id}/maxresdefault.jpg"
    test_topics = [
        {
            "topic": "Introduction to Python",
            "summary": "Python is a high-level programming language known for its readability and versatility.",
            "questions": [
                {"question": "What is Python?", "answer": "Python is a programming language that emphasizes code readability."},
                {"question": "Why use Python?", "answer": "Python is easy to learn, has a large community, and is used in various fields."}
            ]
        }
    ]
    
    html_content = generate_html(test_title, test_topics, test_video_id, test_thumbnail)
    saved = save_html(html_content, "test_summary.html")
    print(f"HTML saved successfully: {saved}") 