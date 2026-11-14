
document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("chat-form");
    const input = document.getElementById("message-input");
    const sendButton = document.getElementById("send-button");
    const messages = document.getElementById("messages");
    const status = document.getElementById("status");

    form.addEventListener("submit", async (event) => {
        event.preventDefault();

      document.querySelectorAll(".suggestion").forEach((button) => {
      button.addEventListener("click", () => {
        input.value = button.textContent.trim();
        input.focus();
      });
        });

        const question = input.value.trim();
        if (!question) return;

        status.textContent = "Sending your message...";
        sendButton.disabled = true;

        try {
            const response = await fetch("/api/complaint", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ question })
            });

            const result = await response.json();
            if (!response.ok) {
                throw new Error(result.error || `Request failed (${response.status}).`);
            }

            const reply = typeof result === "string"
                ? result
                : Array.isArray(result)
                    ? result[0]
                    : result.reply || result.response || result.message;

            const replyElement = document.createElement("div");
            replyElement.className = "reply";
            replyElement.textContent = reply || "The server returned no reply.";
            messages.append(replyElement);

            input.value = "";
            status.textContent = "";
        } catch (error) {
            status.textContent = error instanceof Error
                ? error.message
                : "Couldn't send your message. Please try again.";
        } finally {
            sendButton.disabled = false;
            input.focus();
        }
    });
});