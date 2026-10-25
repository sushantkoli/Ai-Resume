import io
import pypdf
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sentence_transformers import SentenceTransformer

from database import get_db
from models.resume import Resume

# Initialize the Model: Outputs a 384-dimensional vector matching our DB schema!
model = SentenceTransformer('all-MiniLM-L6-v2') 

router = APIRouter()
ALLOWED_TYPES = ["application/pdf"]

@router.post("/resumes")
async def upload_resume(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
):
    # 1. Early Validation: Check content type header
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=400, 
            detail=f"Unsupported file type: {file.content_type}. Please upload a valid PDF."
        )
        
    # Read the file contents as raw bytes asynchronously
    content = await file.read()

    try:
        # Wrap the bytes in io.BytesIO so the PDF parser can read it like a file in memory
        pdf_content = io.BytesIO(content)

        # Use pypdf.PdfReader to read the in-memory stream
        reader = pypdf.PdfReader(pdf_content)

        # Extract the text from all the pages
        extracted_pages = []
        for page in reader.pages:
            text = page.extract_text()
            if text:  
                extracted_pages.append(text)

        # Join it into a single string
        full_text = "\n".join(extracted_pages)

        # Generate the Embedding (.tolist() converts numpy array to standard Python list)
        embedding = model.encode(full_text).tolist()
            
        # Save to Database: Create a new Resume instance
        new_resume = Resume(
            filename=file.filename,
            content=full_text,
            embedding=embedding
        )

        db.add(new_resume)             # Add it to the session
        await db.commit()              # Commit the transaction asynchronously
        await db.refresh(new_resume)   # Refresh the object to fetch its new DB ID
            
        # Return a JSON response with the ID and filename
        return JSONResponse(
            content={
                "id": new_resume.id,
                "filename": new_resume.filename
            }
        )

    except pypdf.errors.PdfReadError:
        raise HTTPException(
            status_code=422, 
            detail="The file structure is invalid or corrupt and cannot be parsed as a PDF."
        )
    except Exception as e:
        raise HTTPException(
            status_code=400, 
            detail="An error occurred while processing the file framework."
        )
