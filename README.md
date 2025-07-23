# MindGather

MindGather is an intelligent assistant designed to streamline the initial phases of project planning and research. It automates the process of gathering information from project specifications (PDF documents), conducting targeted web research, scraping relevant data, and then leveraging a large language model to generate detailed technical implementation plans based on a user's proposed solution.

-----

## Features

  * **PDF Document Processing**: Reads and extracts key information from PDF project requirement documents.
  * **Intelligent Information Extraction**: Utilizes Google's Gemini AI to extract critical details like problem statements, requirements, and necessary technologies.
  * **Automated Web Search Query Generation**: Generates precise and technical search queries based on extracted problem descriptions to find relevant online resources.
  * **Targeted Web Research**: Performs web searches using Google Custom Search to gather information.
  * **Web Content Scraping**: Scrapes textual content from relevant web links to build a comprehensive knowledge base.
  * **AI-Powered Plan Generation**: Leverages the Gemini 1.5 Pro model to generate detailed and technical implementation plans, incorporating all gathered information and the user's proposed solution.
  * **Gradio User Interface**: Provides a simple, interactive web interface for users to input their proposed solutions and receive generated plans.

-----

## How it Works

MindGather operates in a multi-step process:

1.  **Read Project Requirements**: It starts by reading your project's requirements from a specified PDF file.
2.  **Extract Core Information**: The system then extracts the core problem, requirements, and technical specifications using an AI model.
3.  **Generate Search Queries**: Based on the extracted problem, it crafts highly specific search queries to find relevant technical information and implementation methods online.
4.  **Perform Web Search**: These queries are used to perform web searches, identifying potential sources of information.
5.  **Scrape Web Data**: It then visits and scrapes textual content from the most relevant web pages, compiling a local knowledge base.
6.  **Generate Implementation Plan**: Finally, you provide your proposed solution, and the AI, using all the gathered data and your input, generates a comprehensive technical implementation plan.
7.  **Interactive UI**: A user-friendly Gradio interface allows you to interact with the plan generation process.

-----

## Setup and Installation

To get MindGather up and running, follow these steps:

### Prerequisites

  * Python 3.8+
  * Google Gemini API Key
  * Google Custom Search API Key
  * Google Custom Search Engine ID (CX)
  * Scrape.do API Token (or a similar web scraping service)

### 1\. Clone the Repository

```bash
git clone <repository_url>
cd mindforge_devtool
```

### 2\. Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

### 3\. Configure Environment Variables

Create a `.env` file in the root directory of the project and add your API keys and IDs:

```
api=YOUR_GEMINI_API_KEY
search_key=YOUR_Google Search_API_KEY
cx=YOUR_GOOGLE_CUSTOM_SEARCH_ENGINE_ID
token=YOUR_SCRAPEDO_API_TOKEN
```

### 4\. Place Your PDF

Ensure your project requirements PDF file (defaulting to `req.pdf`) is in the same directory as the `readDocs.py` script, or update the `file_name` variable in the `main` method to point to your PDF.

-----

## Usage

To start MindGather and launch the Gradio interface:

```bash
python readDocs.py
```

The script will first perform the automated steps of reading the PDF, extracting information, searching the web, and scraping data. You'll see progress messages in your console:

```
Step 1- finished
Step 2- finished
Step 3- finished
Step 4- finished
Step 5- finished
```

Once these steps are complete, a Gradio web interface will open in your browser (or provide a local URL to access it).

1.  **Enter your proposed solution** into the provided text box in the Gradio interface.
2.  Click the **Submit** button (or similar, depending on Gradio's default).
3.  The AI will then generate a detailed technical implementation plan based on your solution and the scraped information, which will be displayed in the output area.

-----

## Project Structure

  * `readDocs.py`: The main script containing the `readDocs` class and its functionalities.
  * `.env`: Environment file for API keys (not included in version control).
  * `req.pdf`: Placeholder for your project requirements PDF.
  * `summary.json` (optional): Stores extracted problem, requirements, and tech details.
  * `queries.txt`: Stores generated search queries.
  * `searchData.json` (optional): Stores raw search results.
  * `info.txt`: Stores scraped web content used by the AI for plan generation.

-----

## Contributing

Feel free to fork this repository, submit pull requests, or open issues for bugs and feature requests.
