from flow import create_youtube_summarizer_flow
import os
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

def main():
    """
    Main entry point for the YouTube Video Summarizer.
    
    This program uses a MapReduce pattern to:
    1. Takes a YouTube video URL as input
    2. Extracts the video transcript
    3. Identifies key topics in the video
    4. Map: Process each topic independently to generate Q&A pairs
    5. Reduce: Combine all processed topics
    6. Creates an HTML page visualizing the summary
    """
    print("=" * 60)
    print("YouTube Video Summarizer (MapReduce Pattern)")
    print("=" * 60)
    
    # Check for OpenAI API key
    if not os.environ.get("OPENAI_API_KEY"):
        print("\nError: OPENAI_API_KEY environment variable not set.")
        print("Please set your API key with:")
        print("  Windows: set OPENAI_API_KEY=your_api_key")
        print("  Linux/Mac: export OPENAI_API_KEY=your_api_key")
        return
    
    # Initialize the shared store
    shared = {
        "url": "",
        "video_id": "",
        "title": "",
        "transcript": "",
        "thumbnail_url": "",  # New field for the video thumbnail
        "topics": [],
        "processed_topics": [],  # New field for MapReduce pattern
        "html": "",
        "output_file": ""
    }

    # Create and run the flow
    logger.info("Creating YouTube summarizer flow with MapReduce pattern")
    youtube_flow = create_youtube_summarizer_flow()
    
    try:
        logger.info("Starting flow execution")
        youtube_flow.run(shared)
        
        # Print a success message with the output location
        if shared.get("output_file") and os.path.exists(shared["output_file"]):
            logger.info(f"Flow completed successfully")
            print(f"\nOpen {shared['output_file']} in your browser to view the summary.")
            
            # Print statistics
            print(f"\nSummary Statistics:")
            print(f"- Processed {len(shared['topics'])} topics")
            qa_count = sum(len(topic.get('questions', [])) for topic in shared['topics'])
            print(f"- Generated {qa_count} questions and answers")
    except Exception as e:
        logger.error(f"Flow execution failed: {e}")
        print(f"\nError: {e}")
        print("Failed to complete the video summarization process.")

if __name__ == "__main__":
    main()
