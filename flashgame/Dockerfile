FROM openai/universe.flashgames:latest

# Update scripts
COPY init /app/universe-envs/flashgames/
COPY launcher.py /app/universe-envs/flashgames/gym_flashgames/launcher.py
RUN chmod +x /app/universe-envs/flashgames/init
RUN chmod +x /app/universe-envs/flashgames/gym_flashgames/launcher.py

RUN mkdir -p /usr/local/openai/git-lfs
RUN touch /usr/local/openai/git-lfs/flashgames.DuskDrive-v0


# For debugging
RUN apt-get install -y vim
RUN apt-get install -y net-tools
RUN apt-get install -y psmisc
RUN apt-get install -y iputils-ping

RUN /app/universe-envs/flashgames/build/bin/unpack-lfs flashgames.DuskDrive-v0

# Remove openssh-server
RUN apt-get remove -y ssh
RUN apt-get autoremove -y

WORKDIR /app

ENTRYPOINT ["/app/universe-envs/flashgames/init"]
CMD ["run"]
