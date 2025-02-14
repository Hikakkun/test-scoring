import fitz  # pymupdf
from pathlib import Path
from datetime import datetime
from PIL import Image, ImageEnhance
import argparse

Image.MAX_IMAGE_PIXELS = None  # 大きな画像処理の警告を無効化


def convert_pdf_to_pixmaps(pdf_path: Path, dpi: int = 400) -> list[fitz.Pixmap]:
    """
    PDFの各ページを指定されたDPIでpixmap形式に変換する関数

    Args:
        pdf_path (Path): PDFファイルのパス
        dpi (int): 画像変換時のDPI (デフォルト: 400)

    Returns:
        list[fitz.Pixmap]: 変換された各ページのPixmapオブジェクトのリスト
    """
    pdf_document: fitz.Document = fitz.open(pdf_path)
    pixmaps: list[fitz.Pixmap] = []
    for i in range(pdf_document.page_count):
        page: fitz.Page = pdf_document[i]
        pix: fitz.Pixmap = page.get_pixmap(dpi=dpi)
        pixmaps.append(pix)
    return pixmaps


def enhance_image_contrast(image_path: Path, magnification: float = 2.0) -> None:
    """
    画像のコントラストを調整して保存する関数

    Args:
        image_path (Path): 入力画像のパス
        magnification (float): コントラストの倍率 (デフォルト: 2.0)
    """
    image = Image.open(image_path)
    grayscale_image = image.convert("L")  # グレースケールに変換
    enhancer = ImageEnhance.Contrast(grayscale_image)
    enhanced_image = enhancer.enhance(magnification)
    enhanced_image.save(image_path)  # 元の画像を上書き保存


def main() -> None:
    """
    コマンドライン引数を処理し、PDFをJPEG画像に変換し、コントラストを調整するメイン関数
    """
    parser = argparse.ArgumentParser(
        description="スキャナから読み取ったPDFをJPEGに変換し、コントラストを上げる"
    )
    parser.add_argument("target_pdf", help="スキャナから読み取ったPDF")
    parser.add_argument(
        "--dpi", type=int, default=400, help="画像変換時のDPI（デフォルト: 400）"
    )
    parser.add_argument(
        "--contrast",
        type=float,
        default=2.0,
        help="コントラスト倍率（デフォルト: 2.0）",
    )
    args = parser.parse_args()

    target_pdf: Path = Path(args.target_pdf)

    # 保存先ディレクトリ作成
    new_dir_path: Path = Path.cwd() / datetime.now().strftime("pdf2jpeg_%m%d_%H%M%S")
    new_dir_path.mkdir(parents=True, exist_ok=True)

    # PDFをpixmapに変換
    pixmaps: list[fitz.Pixmap] = convert_pdf_to_pixmaps(target_pdf, dpi=args.dpi)

    # 各ページをJPEGとして保存し、コントラストを調整
    for i, pix in enumerate(pixmaps):
        print(f"{i + 1:03}ページ変換中")
        file_name: Path = new_dir_path / f"{i + 1:03}.jpeg"
        pix.save(str(file_name))  # `pix.save` は文字列パスが必要
        enhance_image_contrast(file_name, magnification=args.contrast)


if __name__ == "__main__":
    main()
