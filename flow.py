from pocketflow import Flow
from nodes import (
    GetYouTubeURLNode, 
    ExtractTranscriptNode, 
    IdentifyTopicsNode, 
    TopicBatchNode,
    CombineResultsNode,
    CreateHTMLNode
)

def create_youtube_summarizer_flow():
    """
    Create and return a YouTube video summarizing flow using MapReduce pattern.
    
    The flow follows these steps:
    1. Get YouTube URL from user
    2. Extract transcript from the video
    3. Identify key topics in the transcript
    4. Map: Process each topic independently to generate Q&A pairs (BatchNode)
    5. Reduce: Combine all processed topics
    6. Create HTML output to visualize the summary
    """
    # Create nodes
    get_url_node = GetYouTubeURLNode()
    extract_transcript_node = ExtractTranscriptNode(max_retries=2)
    identify_topics_node = IdentifyTopicsNode(max_retries=2)
    
    # Map phase: Process each topic in batch
    topic_batch_node = TopicBatchNode(max_retries=2)
    
    # Reduce phase: Combine results
    combine_results_node = CombineResultsNode()
    
    # Final output
    create_html_node = CreateHTMLNode()
    
    # Connect nodes in sequence according to MapReduce pattern
    get_url_node >> extract_transcript_node >> identify_topics_node
    identify_topics_node >> topic_batch_node >> combine_results_node
    combine_results_node >> create_html_node
    
    # Create flow starting with input node
    return Flow(start=get_url_node)

# Create the flow for easy import in main.py
youtube_summarizer_flow = create_youtube_summarizer_flow()