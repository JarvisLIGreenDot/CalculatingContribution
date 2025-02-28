from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from datetime import datetime
from business.contributions_service import ContributionsService

router = APIRouter(
    prefix="/contributions",
    tags=["contributions"]
)

@router.get("/export")
async def export_contributions(days: int = 30):
    """
    Export GitHub contributions to CSV file
    
    Args:
        days: Number of days to look back (default: 30)
    
    Returns:
        FileResponse: CSV file download
    """
    try:
        service = ContributionsService()
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