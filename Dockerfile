# ==============================================================
# Hermes Agent + On-Server Web Chat (chat.html) for Render.com
# ==============================================================
FROM nousresearch/hermes-agent:latest

USER root

# Create directory structure and set open permissions for data
RUN mkdir -p /opt/hermes/web /opt/hermes/deploy /opt/data && \
    chmod -R 777 /opt/data

# Copy custom web chat and server proxy
COPY web/chat.html /opt/hermes/web/chat.html
COPY deploy/server.py /opt/hermes/deploy/server.py
COPY deploy/start.sh /opt/hermes/deploy/start.sh

RUN chmod +x /opt/hermes/deploy/start.sh

# Expose Render default port
EXPOSE 10000

# Start Hermes gateway + web proxy
CMD ["/opt/hermes/deploy/start.sh"]
