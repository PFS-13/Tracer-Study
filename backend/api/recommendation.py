from fastapi import APIRouter
router = APIRouter(
    prefix="/api",
    tags=["Dataset"]
)
@router.get("/columns")
def get_columns(
    dataset: str
):
    columns = None
    if dataset == "tracer":
        columns = [
            {"field": "Nama","type": "nominal"},
            {"field": "Program_Studi","type": "nominal"},
            {"field": "Tahun_Lulus","type": "temporal"},
            {"field": "IPK","type": "quantitative"},
            {"field": "Status_Saat_Ini","type": "nominal"},
            {"field": "Waktu_Tunggu_Bulan","type": "quantitative"},
            {"field": "Lokasi_Kerja","type": "nominal"
            }
        ]

    return columns