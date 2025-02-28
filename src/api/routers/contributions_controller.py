from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from datetime import datetime
from repos.DataAccess import db
from business.contributions_service import ContributionsService

router = APIRouter(
    prefix="/contributions",
    tags=["contributions"]
)

@router.get("/export")
async def export_contributions(
    days: int = 7,
    db: Session = Depends(db.get_db)
):
    """
    Export GitHub contributions to CSV file
    
    Args:
        days: Number of days to look back (default: 7)
    
    Returns:
        FileResponse: CSV file download
    """
    try:
        service = ContributionsService(db)
        filepath = await service.export_contributions_csv(days=days)
        
        return FileResponse(
            filepath,
            media_type='text/csv',
            filename=f"github_contributions_{datetime.now().strftime('%Y%m%d')}.csv"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )