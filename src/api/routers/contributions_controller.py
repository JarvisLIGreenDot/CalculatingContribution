from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from datetime import datetime
from business.contributions_service import ContributionsService

router = APIRouter(
    prefix="/contributions",
    tags=["contributions"]
)

@router.get("/export")
async def export_contributions(days: int = 7):
    """
    Export GitHub contributions to CSV file
    
    Args:
        days: Number of days to look back (default: 30)
    
    Returns:
        StreamingResponse: CSV file download
    """
    try:
        service = ContributionsService()
        csv_content = await service.export_contributions_csv(days=days)
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"github_contributions_{timestamp}.csv"
        
        return StreamingResponse(
            iter([csv_content.getvalue()]),
            media_type='text/csv',
            headers={
                'Content-Disposition': f'attachment; filename="{filename}"'
            }
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )