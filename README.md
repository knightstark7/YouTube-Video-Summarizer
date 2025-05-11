# YouTube Video Summarizer

A Python application that summarizes YouTube videos using a MapReduce pattern to extract key topics, and generate questions and answers for each topic.

## Features

- Takes a YouTube video URL as input
- **Multilingual Support**: Works with both English and Vietnamese videos, with fallback to any available language
- Extracts the video transcript with smart language detection
- Identifies key topics from the video content
- Uses MapReduce pattern to process each topic independently
- Generates relevant questions and answers for each topic
- **Rich Visual Output**: Creates a beautifully formatted HTML page with video thumbnail and direct link
- Comprehensive error handling for various transcript availability scenarios

## Screenshots

The generated HTML summary includes:
- The video thumbnail with a direct link to YouTube
- Key topics extracted from the video
- Detailed summaries of each topic
- Insightful questions and answers for each topic
- Clean, responsive design for easy reading

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/youtube-video-summarizer.git
   cd youtube-video-summarizer
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Set your OpenAI API key:
   - Windows: `set OPENAI_API_KEY=your_api_key`
   - Linux/Mac: `export OPENAI_API_KEY=your_api_key`

## Usage

Run the application:
```
python main.py
```

Follow the prompts to enter a YouTube video URL. The application will process the video and generate an HTML summary file in the current directory.

## How It Works

This application uses PocketFlow, a minimalist LLM framework, to create a MapReduce pipeline that:

1. Extracts transcripts from YouTube videos using `youtube-transcript-api` with multilingual support
2. Uses OpenAI's GPT models to analyze the content and identify key topics
3. **Map Phase**: Processes each topic independently to generate questions and answers
4. **Reduce Phase**: Combines all processed topics into a coherent structure
5. Creates an HTML visualization with the video thumbnail and all processed information

### MapReduce Benefits

- **Modularity**: Each topic is processed independently, making the code more maintainable
- **Error Isolation**: Issues with one topic won't affect the processing of others
- **Scalability**: The design can be extended to support parallel processing of topics
- **Clarity**: Clearer separation of concerns in the code structure

## Requirements

- Python 3.7+
- OpenAI API key
- Internet connection to access YouTube and OpenAI services

## Limitations

- Only works with YouTube videos that have available transcripts/captions
- Processing time depends on video length and OpenAI API response time
- May occasionally generate irrelevant topics if the transcript is unclear or highly technical
- Some auto-generated transcripts may have reduced accuracy

## License

MIT
