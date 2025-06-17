from pytubefix import YouTube, Playlist
from moviepy import AudioFileClip
from pyfiglet import Figlet
from colorama import init, Fore, Style
import os
import re


def limpar_titulo(titulo):
    return re.sub(r'[\\/*?:"<>|]', "_", titulo.replace(" ", "_"))


def baixar_video(url, formato="mp4", destino="downloads", subpasta_extra=None):
    try:
        print(f"\n➡️ Tentando baixar: {url}")
        yt = YouTube(url)
        titulo = limpar_titulo(yt.title)
        print(f"📥 Baixando: {yt.title}")

        if formato == "mp3":
            stream = yt.streams.filter(only_audio=True).first()
            if stream is None:
                print("❌ Nenhum stream de áudio encontrado.")
                return

            pasta_destino = os.path.join(destino, "musica")
        else:
            stream = yt.streams.get_highest_resolution()
            if stream is None:
                print("❌ Nenhum stream de vídeo encontrado.")
                return

            pasta_destino = os.path.join(destino, "video")

        if subpasta_extra:
            pasta_destino = os.path.join(pasta_destino, limpar_titulo(subpasta_extra))

        os.makedirs(pasta_destino, exist_ok=True)

        if formato == "mp3":
            out_file = stream.download(
                output_path=pasta_destino, filename=f"{titulo}.mp4"
            )
            mp3_file = os.path.join(pasta_destino, f"{titulo}.mp3")
            print("🎵 Convertendo para mp3...")
            audio_clip = AudioFileClip(out_file)
            audio_clip.write_audiofile(mp3_file)
            audio_clip.close()
            os.remove(out_file)
            print(f"✅ Download concluído: {mp3_file}")
        else:
            mp4_file = stream.download(
                output_path=pasta_destino, filename=f"{titulo}.mp4"
            )
            print(f"✅ Download concluído: {mp4_file}")

    except Exception as e:
        print(f"❌ Erro ao baixar o vídeo: {e}")


def baixar_playlist(url, formato="mp4", destino="downloads"):
    try:
        playlist = Playlist(url)
        nome_playlist = playlist.title or "playlist_sem_nome"
        print(f"\n📃 Playlist encontrada: {nome_playlist}")
        print(f"🎬 Total de vídeos: {len(playlist.video_urls)}")

        for video_url in playlist.video_urls:
            baixar_video(video_url, formato, destino, subpasta_extra=nome_playlist)

    except Exception as e:
        print(f"❌ Erro ao processar a playlist: {e}")


def executar_download():
    url = input("🔗 Insira a URL do vídeo ou playlist do YouTube: ").strip()
    if not url.startswith("http"):
        print("❌ URL inválida.")
        return

    formato = input("🎧 Deseja baixar como MP3? (s/n): ").strip().lower()
    tipo = "mp3" if formato == "s" else "mp4"

    destino = input("📁 Pasta de destino (deixe em branco para 'downloads'): ").strip()
    if not destino:
        destino = os.path.join(os.path.dirname(os.path.abspath(__file__)), "downloads")

    if not os.path.exists(destino):
        os.makedirs(destino)

    if "playlist" in url.lower():
        baixar_playlist(url, tipo, destino)
    else:
        baixar_video(url, tipo, destino)


def main():
    init(autoreset=True)  # Inicializa colorama

    f = Figlet(font="slant")
    banner = f.renderText("HelcioTube")

    # Estilo principal: vermelho YouTube + negrito
    print(Fore.RED + Style.BRIGHT + banner)

    # Subtítulo branco sobre fundo escuro (simulado)
    print(
        Fore.WHITE
        + Style.BRIGHT
        + "📽️  Versão 1.0.2025 | Desenvolvido por Hélcio Nicolau\n"
    )

    while True:
        executar_download()
        repetir = (
            input(Fore.LIGHTBLACK_EX + "\n🔁 Deseja fazer outro download? (s/n): ")
            .strip()
            .lower()
        )
        if repetir != "s":
            print(Fore.RED + "👋 Programa encerrado. Até logo!")
            break


if __name__ == "__main__":
    main()
