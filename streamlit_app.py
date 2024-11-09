import streamlit as st
from dotenv import load_dotenv

from app import build_graph
import json
from config_loader import ConfigLoader
import time
from datetime import datetime
import os

# Load environment variables at the start of your app
load_dotenv()

# Now you can access the API key from anywhere using:
api_key = os.getenv('GROQ_API_KEY')

# Verify the API key is loaded
if not api_key:
    raise ValueError("GROQ_API_KEY not found in environment variables")

def setup_logging():
    """Create logs directory if it doesn't exist"""
    if not os.path.exists('logs'):
        os.makedirs('logs')


def log_output(output_data, session_id):
    """Log output to a file"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"logs/session_{session_id}_{timestamp}.txt"

    with open(filename, 'a') as f:
        f.write(f"\n{'=' * 50}\n")
        f.write(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(json.dumps(output_data, indent=2))
        f.write("\n")

    return filename


def main():
    setup_logging()

    # Generate a unique session ID
    if 'session_id' not in st.session_state:
        st.session_state.session_id = int(time.time())

    st.set_page_config(
        page_title="AI Agents Task Decomposition System",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Light theme-friendly styling
    # Only showing the modified styling section - the rest of the code remains the same

    # Updated styling for better readability
    st.markdown("""
            <style>
            /* Main container styling */
            .main {
                background-color: #ffffff !important;
                padding: 2rem;
                color: #000000 !important;
            }

            /* Force dark text on white background */
            .stApp {
                background-color: #ffffff !important;
                max-width: 1200px;
                margin: 0 auto;
            }

            /* Make all text black by default */
            .element-container, .stMarkdown, .stTextArea textarea {
                color: #000000 !important;
            }

            /* Style the header */
            .custom-header {
                color: #000000 !important;
                padding: 1rem 0;
                border-bottom: 2px solid #333;
                margin-bottom: 2rem;
                font-weight: bold;
            }

            /* Style the info box */
            .info-box {
                background-color: #ffffff !important;
                padding: 1rem;
                border-radius: 5px;
                margin: 1rem 0;
                border: 1px solid #333;
                color: #000000 !important;
            }

            /* Style the output box */
            .output-box {
                background-color: #ffffff !important;
                padding: 1rem;
                border-radius: 5px;
                margin: 1rem 0;
                border: 1px solid #333;
                max-height: 400px;
                overflow-y: auto;
                color: #000000 !important;
            }

            /* Force text input areas to have black text */
            .stTextArea label, .stTextInput label {
                color: #000000 !important;
            }

            .stTextArea textarea, .stTextInput input {
                color: #000000 !important;
                background-color: #ffffff !important;
            }

            /* Style the sidebar */
            .css-1d391kg {
                background-color: #ffffff !important;
            }

            .sidebar .sidebar-content {
                background-color: #ffffff !important;
            }

            /* Make tab text visible */
            .stTabs [data-baseweb="tab"] {
                color: #000000 !important;
            }

            /* Style the button */
            .stButton > button {
                color: #ffffff !important;
                background-color: #2e6be6 !important;
                border: none;
                padding: 0.5rem 1rem;
                font-weight: bold;
            }

            /* Override any dark mode text */
            * {
                color-scheme: light !important;
            }

            /* Make sure headers are visible */
            h1, h2, h3, h4, h5, h6 {
                color: #000000 !important;
            }

            /* Style placeholder text */
            ::placeholder {
                color: #666666 !important;
                opacity: 1 !important;
            }

            /* Style the JSON output */
            pre {
                background-color: #f8f9fa !important;
                color: #000000 !important;
                border: 1px solid #e9ecef;
                border-radius: 5px;
            }
            </style>
        """, unsafe_allow_html=True)

    # Header
    st.title("AI Agents Task Decomposition & Parallel Execution System via Map-Reduce")

    # Sidebar with example problems
    st.sidebar.header("Example Problems")
    example_problems = {
        "Healthcare Resource Optimization": {
            "input": "Optimize resource allocation in a large hospital network",
            "considerations": "patient care quality, staff workload, equipment utilization, emergency preparedness, budget constraints"
        },
        "Supply Chain Enhancement": {
            "input": "Modernize global supply chain operations for a retail company",
            "considerations": "inventory management, shipping costs, delivery times, sustainability, supplier reliability"
        },
        "Smart City Development": {
            "input": "Implement smart city solutions for traffic management",
            "considerations": "real-time monitoring, data privacy, infrastructure costs, citizen convenience, environmental impact"
        },
        "Educational System Reform": {
            "input": "Design a hybrid learning system for universities",
            "considerations": "student engagement, technology infrastructure, teaching effectiveness, accessibility, cost efficiency"
        }
    }

    selected_example = st.sidebar.selectbox(
        "Select an example problem",
        ["Custom Input"] + list(example_problems.keys())
    )

    # Main content area
    col1, col2 = st.columns([2, 1])

    with col1:
        st.header("Problem Definition", divider="blue")

        # Set input fields based on selection
        if selected_example != "Custom Input":
            problem = example_problems[selected_example]
            input_text = st.text_area("Problem Statement", value=problem["input"], height=100)
            considerations = st.text_area("Key Considerations", value=problem["considerations"], height=100)
        else:
            input_text = st.text_area(
                "Problem Statement",
                placeholder="Describe the problem you want to solve...",
                height=100
            )
            considerations = st.text_area(
                "Key Considerations",
                placeholder="List key factors to consider, separated by commas...",
                height=100
            )

    with col2:
        st.markdown("""
        <div class='info-box'>
        <h4>Tips for Good Problem Definition:</h4>
        <ul>
            <li>Be specific and clear about the challenge</li>
            <li>Include relevant context</li>
            <li>Consider multiple stakeholders</li>
            <li>Think about both short and long-term impacts</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

    # Process button
    if st.button("Generate Solutions", type="primary"):
        if input_text and considerations:
            try:
                progress_bar = st.progress(0)
                status_text = st.empty()

                # Create a new log file for this session
                log_files = []

                with st.spinner("Processing your request... This may take a few minutes."):
                    # Initialize the graph
                    graph = build_graph()

                    # Prepare input
                    input_data = {
                        "input": input_text,
                        "considerations": considerations
                    }

                    # Log input
                    log_files.append(log_output({"input_data": input_data}, st.session_state.session_id))

                    # Initialize output containers
                    output_tabs = st.tabs([
                        "Generated Solutions",
                        "Solution Evaluation",
                        "Deep Analysis",
                        "Final Rankings"
                    ])

                    # Process and display results
                    step = 0
                    for output in graph.stream(input_data):
                        step += 1
                        progress_bar.progress(step * 0.25)

                        # Log the output
                        log_file = log_output(output, st.session_state.session_id)
                        log_files.append(log_file)

                        # Display in appropriate tab
                        if "solutions" in output:
                            with output_tabs[0]:
                                st.json(output["solutions"])
                            status_text.text("Generated initial solutions...")
                        elif "reviews" in output:
                            with output_tabs[1]:
                                st.json(output["reviews"])
                            status_text.text("Evaluated solutions...")
                        elif "deep_thoughts" in output:
                            with output_tabs[2]:
                                st.json(output["deep_thoughts"])
                            status_text.text("Completed deep analysis...")
                        elif "ranked_solutions" in output:
                            with output_tabs[3]:
                                st.json(output["ranked_solutions"])
                            status_text.text("Finished ranking solutions...")

                    progress_bar.progress(100)
                    st.success("Analysis completed successfully!")

                    # Display combined log file
                    st.header("Execution Log", divider="blue")
                    log_content = ""
                    for log_file in log_files:
                        with open(log_file, 'r') as f:
                            log_content += f.read() + "\n"

                    st.code(log_content, language="json")

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                # Log error
                log_output({"error": str(e)}, st.session_state.session_id)
        else:
            st.warning("Please provide both a problem statement and considerations.")


if __name__ == "__main__":
    main()