from pocketflow import Node, BatchNode
from utils.youtube_utils import extract_video_id, get_transcript, get_video_title, get_thumbnail_url
from utils.llm_utils import call_llm, extract_topics_from_llm_response
from utils.html_utils import generate_html, save_html
import yaml

class GetYouTubeURLNode(Node):
    def exec(self, _):
        """Get YouTube URL from user."""
        url = input("Enter YouTube video URL: ")
        return url
        
    def post(self, shared, prep_res, exec_res):
        shared["url"] = exec_res
        return "default"

class ExtractTranscriptNode(Node):
    def prep(self, shared):
        """Get URL from shared store."""
        return shared["url"]
        
    def exec(self, url):
        """Extract transcript from YouTube video."""
        video_id = extract_video_id(url)
        if not video_id:
            raise ValueError(f"Could not extract video ID from URL: {url}")
            
        transcript = get_transcript(video_id)
        if not transcript:
            raise ValueError(f"Could not get transcript for video ID: {video_id}")
            
        title = get_video_title(video_id)
        thumbnail_url = get_thumbnail_url(video_id)
        return video_id, transcript, title, thumbnail_url
        
    def post(self, shared, prep_res, exec_res):
        video_id, transcript, title, thumbnail_url = exec_res
        shared["video_id"] = video_id
        shared["transcript"] = transcript
        shared["title"] = title
        shared["thumbnail_url"] = thumbnail_url
        shared["output_file"] = f"video_summary_{video_id}.html"
        return "default"

class IdentifyTopicsNode(Node):
    def prep(self, shared):
        """Get transcript from shared store."""
        return shared["transcript"], shared["title"]
        
    def exec(self, inputs):
        """Identify key topics in the video."""
        transcript, title = inputs
        
        # Create prompt for topic identification
        prompt = f"""
        Analyze the following transcript from a YouTube video titled "{title}" and identify 3-5 main topics.
        For each topic, provide a brief summary.

        TRANSCRIPT:
        {transcript}

        Format your response as YAML:
        ```yaml
        topics:
          - topic: "Topic 1 Title"
            summary: "Brief summary of Topic 1"
          - topic: "Topic 2 Title"
            summary: "Brief summary of Topic 2"
          - topic: "Topic 3 Title"
            summary: "Brief summary of Topic 3"
        ```
        """
        
        response = call_llm(prompt)
        return extract_topics_from_llm_response(response)
        
    def post(self, shared, prep_res, exec_res):
        # Initialize topics with empty questions list
        topics = exec_res
        for topic in topics:
            topic["questions"] = []
            
        shared["topics"] = topics
        return "default"

class TopicBatchNode(BatchNode):
    def prep(self, shared):
        """Return topics as an iterable for batch processing."""
        topics = shared["topics"]
        transcript = shared["transcript"]
        
        # For each topic, we'll pass both the topic and the transcript
        return [(topic, transcript) for topic in topics]
    
    def exec(self, batch_item):
        """Process a single topic to generate Q&A pairs."""
        topic, transcript = batch_item
        
        # Generate Q&A pairs for this specific topic
        topic_prompt = f"""
        Based on this transcript portion about "{topic['topic']}", generate 2-3 insightful questions and answers.
        
        TOPIC: {topic['topic']}
        SUMMARY: {topic['summary']}
        
        TRANSCRIPT:
        {transcript}
        
        Format your response as YAML:
        ```yaml
        questions:
          - question: "First question about {topic['topic']}?"
            answer: "Comprehensive answer to the first question."
          - question: "Second question about {topic['topic']}?"
            answer: "Comprehensive answer to the second question."
        ```
        """
        
        response = call_llm(topic_prompt)
        try:
            # Extract YAML content
            if "```yaml" in response:
                yaml_content = response.split("```yaml")[1].split("```")[0].strip()
            elif "```" in response:
                yaml_content = response.split("```")[1].split("```")[0].strip()
            else:
                yaml_content = response.strip()
            
            qa_data = yaml.safe_load(yaml_content)
            
            # Update topic with questions
            if isinstance(qa_data, dict) and "questions" in qa_data:
                topic["questions"] = qa_data["questions"]
            
        except Exception as e:
            print(f"Error processing Q&A for topic '{topic['topic']}': {e}")
            topic["questions"] = [{"question": "Error generating questions", "answer": "Please try again."}]
        
        return topic
    
    def post(self, shared, prep_res, exec_res_list):
        """Store the processed topics with their Q&A pairs."""
        shared["processed_topics"] = exec_res_list
        return "default"

class CombineResultsNode(Node):
    def prep(self, shared):
        """Get processed topics from shared store."""
        return shared["processed_topics"]
    
    def exec(self, processed_topics):
        """Combine and organize all processed topics."""
        # This is a simple passthrough since our topics are already processed
        # In a more complex scenario, we might do additional processing here
        return processed_topics
    
    def post(self, shared, prep_res, exec_res):
        """Store combined topics back to shared store."""
        shared["topics"] = exec_res
        print(f"Successfully processed {len(exec_res)} topics with Q&A pairs")
        return "default"

class CreateHTMLNode(Node):
    def prep(self, shared):
        """Get topics, title, and thumbnail URL from shared store."""
        return shared["topics"], shared["title"], shared["output_file"], shared["video_id"], shared["thumbnail_url"]
        
    def exec(self, inputs):
        """Generate HTML for the video summary."""
        topics, title, output_file, video_id, thumbnail_url = inputs
        
        # Generate HTML
        html_content = generate_html(title, topics, video_id, thumbnail_url)
        
        # Save HTML to file
        success = save_html(html_content, output_file)
        
        return html_content, output_file, success
        
    def post(self, shared, prep_res, exec_res):
        html_content, output_file, success = exec_res
        
        shared["html"] = html_content
        
        if success:
            print(f"\nSummary successfully generated and saved to {output_file}")
        else:
            print("\nError: Failed to save HTML file.")
            
        return "default"