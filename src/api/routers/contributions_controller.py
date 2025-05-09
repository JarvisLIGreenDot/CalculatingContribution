from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from datetime import datetime
from business.contributions_service import ContributionsService

router = APIRouter(
    prefix="/contributions",
    tags=["contributions"]
)

@router.get("/export")
async def export_contributions(days: int = 7, role_key: int = 1, team_key: int = 1):
    """
    Export GitHub contributions to CSV file
    
    Args:
        days: Number of days to look back (default: 30)
        RoleKey: Role key to filter users by (default: 1)
        TeamKey: Team key to filter users by (default: 1)
    
    Returns:
        StreamingResponse: CSV file download
    """
    try:
        service = ContributionsService()
        csv_content = await service.export_contributions_csv(
            days=days, role_key=role_key, team_key=team_key
        )
        
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

@router.get("/export/details/{username}")
async def export_user_contribution_details(username: str, days: int = 7):
    """
    Export detailed GitHub contributions for a specific user to CSV
    
    Args:
        username: GitHub username to get details for
        days: Number of days to look back (default: 7)
    
    Returns:
        StreamingResponse: CSV file download with detailed contribution data
    """
    try:
        service = ContributionsService()
        csv_content = await service.export_contribution_details_csv(
            days=days,
            username=username
        )
        
        # Generate filename with timestamp and username
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"github_contributions_details_{username}_{timestamp}.csv"
        
        return StreamingResponse(
            iter([csv_content.getvalue()]),
            media_type='text/csv',
            headers={
                'Content-Disposition': f'attachment; filename="{filename}"'
            }
        )
        
    except HTTPException as he:
        # Re-raise HTTP exceptions from the service
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to export contribution details: {str(e)}"
        )