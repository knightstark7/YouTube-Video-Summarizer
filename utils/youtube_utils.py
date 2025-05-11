from youtube_transcript_api import YouTubeTranscriptApi
import re

def extract_video_id(url):
    """Extract YouTube video ID from URL."""
    video_id_match = re.search(r'(?:v=|\/)([0-9A-Za-z_-]{11}).*', url)
    if video_id_match:
        return video_id_match.group(1)
    return None

def get_thumbnail_url(video_id):
    """
    Get the thumbnail URL for a YouTube video.
    YouTube provides several thumbnail resolutions, we'll get the highest quality one.
    """
    # YouTube thumbnail URL format - maxresdefault is highest quality
    # Other options include: default.jpg, hqdefault.jpg, mqdefault.jpg, sddefault.jpg
    return f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"

def get_transcript(video_id):
    """
    Get transcript from YouTube video.
    Tries to fetch in both English and Vietnamese, and falls back to any available language.
    """
    try:
        # First try: specified languages (English and Vietnamese)
        try:
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['en', 'vi'])
            transcript_text = ' '.join([item['text'] for item in transcript_list])
            print(f"Successfully retrieved transcript in English or Vietnamese")
            return transcript_text
        except Exception as e:
            print(f"Could not retrieve transcript in English or Vietnamese: {e}")
            
        # Second try: auto-generated transcripts for these languages
        try:
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['en-US', 'vi', 'en'])
            transcript_text = ' '.join([item['text'] for item in transcript_list])
            print(f"Successfully retrieved auto-generated transcript")
            return transcript_text
        except Exception as e:
            print(f"Could not retrieve auto-generated transcript: {e}")
        
        # Last resort: try any available transcript
        print("Attempting to retrieve transcript in any available language...")
        available_transcripts = YouTubeTranscriptApi.list_transcripts(video_id)
        
        # Try to find manual transcripts first (they're usually better quality)
        for transcript in available_transcripts:
            if not transcript.is_generated:
                transcript_data = transcript.fetch()
                transcript_text = ' '.join([item['text'] for item in transcript_data])
                print(f"Retrieved manual transcript in language: {transcript.language_code}")
                return transcript_text
        
        # If no manual transcript, get any generated one
        for transcript in available_transcripts:
            transcript_data = transcript.fetch()
            transcript_text = ' '.join([item['text'] for item in transcript_data])
            print(f"Retrieved generated transcript in language: {transcript.language_code}")
            return transcript_text
            
        raise Exception("No transcripts found in any language")
            
    except Exception as e:
        print(f"Error fetching transcript: {e}")
        return None
        
def get_video_title(video_id):
    """Get the title of a YouTube video."""
    # In a real implementation, this would fetch the title from YouTube API
    # For simplicity, we'll return a placeholder
    return f"YouTube Video ({video_id})"

if __name__ == "__main__":
    # Test with a sample YouTube URL
    test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    video_id = extract_video_id(test_url)
    if video_id:
        transcript = get_transcript(video_id)
        print(f"Video ID: {video_id}")
        print(f"Thumbnail URL: {get_thumbnail_url(video_id)}")
        print(f"Transcript preview: {transcript[:300]}...") 