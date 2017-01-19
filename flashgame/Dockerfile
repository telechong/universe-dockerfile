FROM openai/universe.flashgames:latest

# Update scripts
COPY init /app/universe-envs/flashgames/
COPY launcher.py /app/universe-envs/flashgames/gym_flashgames/launcher.py
RUN chmod +x /app/universe-envs/flashgames/init
RUN chmod +x /app/universe-envs/flashgames/gym_flashgames/launcher.py

RUN mkdir -p /usr/local/openai/git-lfs
RUN touch /usr/local/openai/git-lfs/flashgames.DuskDrive-v0

# For debugging
RUN apt-get update; \
    apt-get upgrade -y; \
    apt-get install -y vim net-tools psmisc iputils-ping

RUN /app/universe-envs/flashgames/build/bin/unpack-lfs flashgames.DuskDrive-v0

# Remove openssh-server
RUN apt-get remove -y openssh-server; \
    apt-get autoremove -y

WORKDIR /app

ENTRYPOINT ["/app/universe-envs/flashgames/init"]
CMD ["run"]
