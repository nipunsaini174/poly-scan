export class PolyScanService {
    constructor(onMessage, onError, onClose) {
      this.url = 'ws://127.0.0.1:8000/api/v1/ws/analyze';
      this.onMessage = onMessage;
      this.onError = onError;
      this.onClose = onClose;
      this.ws = null;
    }
  
    connect() {
      this.ws = new WebSocket(this.url);
      this.ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          this.onMessage(data);
        } catch (e) {
          console.error("Failed to parse websocket message", e);
        }
      };
      this.ws.onerror = (error) => {
        if (this.onError) this.onError(error);
      };
      this.ws.onclose = () => {
        if (this.onClose) this.onClose();
      };
    }
  
    analyze(codeA, langA, codeB, langB) {
      if (this.ws && this.ws.readyState === WebSocket.OPEN) {
        this.ws.send(JSON.stringify({
          code_a: codeA,
          language_a: langA,
          code_b: codeB,
          language_b: langB
        }));
      } else {
        this.connect();
        // Wait for connect
        this.ws.onopen = () => {
            this.ws.send(JSON.stringify({
                code_a: codeA,
                language_a: langA,
                code_b: codeB,
                language_b: langB
            }));
        };
      }
    }
  
    disconnect() {
      if (this.ws) {
        this.ws.close();
      }
    }
  }
