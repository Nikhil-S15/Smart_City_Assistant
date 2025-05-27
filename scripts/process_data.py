import json
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pathlib import Path

def load_and_chunk_data(input_path, output_path):
    with open(input_path, 'r') as f:
        data = json.load(f)
    
    documents = []
    metadata = []
    
    for category, items in data['knowledge_base'].items():
        if category == 'test_queries':
            continue
            
        for item in items:
            content = f"Title: {item.get('title', '')}\n"
            content += f"Category: {item.get('category', '')}\n"
            content += f"Content: {item.get('content', '')}\n"
            
            for field in ['contact', 'address', 'hours', 'phone', 'website']:
                if field in item:
                    content += f"{field.capitalize()}: {item[field]}\n"
            
            documents.append(content)
            metadata.append({
                "id": item.get("id", ""),
                "title": item.get("title", ""),
                "category": item.get("category", ""),
                "source": category
            })
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    
    chunks = text_splitter.create_documents(documents, metadatas=metadata)
    
    Path(output_path).parent.mkdir(exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump([{
            "text": chunk.page_content,
            "metadata": chunk.metadata
        } for chunk in chunks], f, indent=2)
    
    print(f"✅ Processed {len(chunks)} document chunks.")

if __name__ == "__main__":
    input_path = "data/smart_city_data.json"
    output_path = "data/processed/chunks.json"
    load_and_chunk_data(input_path, output_path)