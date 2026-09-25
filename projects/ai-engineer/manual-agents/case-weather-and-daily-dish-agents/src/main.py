import sys
from pathlib import Path

# Adds the 'src' directory itself to sys.path so 'core' and 'app' can be imported directly
src_dir = Path(__file__).resolve().parent
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

from src.app.configs.settings import Settings  # noqa: E402
from src.core.domain.orchestrator.chatbot_orchestrator import ChatbotOrchestrator  # noqa: E402
from src.core.layer.data.pdf_loader import PdfFaqLoader  # noqa: E402
from src.core.layer.logging.app_logger import AppLogger  # noqa: E402


def main() -> None:
    """Application bootstrap and interactive console loop runner."""
    logger = AppLogger.get_logger("MainBootstrapper")
    logger.info("🚀 Initializing The Daily Dish Chatbot System...")

    try:
        faq_data = PdfFaqLoader.parse_faq(Settings.FAQ_PDF_PATH)
    except Exception as e:
        logger.error("❌ Failed to load and parse FAQ PDF document: %s", e)
        return

    orchestrator = ChatbotOrchestrator(faq_data)

    # Interactive Command Panel Banner via Logger
    logger.info("=" * 60)
    logger.info("🍽️  WELCOME TO THE DAILY DISH INTELLIGENT CHATBOT 🤖")
    logger.info("=" * 60)
    logger.info("📋 Available Commands:")
    logger.info("   • Type any question about our restaurant menu, hours, or policies 📖")
    logger.info("   • Ask about the current weather conditions (e.g., 'How is the weather?') 🌤️")
    logger.info("   • 'exit', 'quit', or 'bye' -> Safely terminates the session 👋")
    logger.info("=" * 60)

    logger.info("🎯 Chatbot orchestrator is ready and listening for queries.")

    while True:
        try:
            user_input = input("💬 You: ").strip()
            if not user_input:
                continue

            if user_input.lower() in ["exit", "quit", "bye"]:
                logger.info("👋 Chatbot: Thanks for visiting The Daily Dish! Have a great day!")
                break

            response = orchestrator.handle_question(user_input)
            logger.info("🤖 Chatbot: %s", response)

        except (KeyboardInterrupt, EOFError):
            logger.info("👋 Chatbot: Session interrupted by user. Goodbye!")
            break


if __name__ == "__main__":
    main()
