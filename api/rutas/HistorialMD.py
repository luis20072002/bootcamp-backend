from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session


from ..database.database import get_db
from ..model.HistorialEdificioAuxiliar import HistorialEdificioAuxiliar
from ..model.Usuario import Usuario
from ..schemas.Historial_SCH import HistorialEdificioAuxiliarResponse
from ..auth.dependencies import solo_admin


router = APIRouter(prefix="/historial", tags=["Historial"])


@router.get("/auxiliar/{id_usuario}", response_model=list[HistorialEdificioAuxiliarResponse])
def get_historial_auxiliar(
    id_usuario: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(solo_admin)
):
    usuario = db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return (
        db.query(HistorialEdificioAuxiliar)
        .filter(HistorialEdificioAuxiliar.id_usuario == id_usuario)
        .order_by(HistorialEdificioAuxiliar.fecha_cambio.desc())
        .all()
    )
