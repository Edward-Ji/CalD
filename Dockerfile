FROM alpine:latest

# Add required packages
RUN apk add alpine-sdk openrc sudo

# Prepare OpenRC
RUN mkdir /run/openrc && touch /run/openrc/softlevel

# Setup system and builder account
RUN adduser -D -g '' builder
RUN echo "builder ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers
USER builder
RUN sudo addgroup builder abuild
RUN sudo mkdir -p /var/cache/distfiles
RUN sudo chmod a+w /var/cache/distfiles
RUN abuild-keygen -a -i -n

# Copy build contents to builder home
WORKDIR /home/builder
COPY --chown=builder dockerentry ./
COPY --chown=builder *.py ./
COPY --chown=builder build ./build

# Run build and install
WORKDIR build
RUN abuild checksum && abuild -r
RUN sudo apk add --repository /home/builder/packages/builder cald

# Entry with daemon started
WORKDIR /home/builder
ENTRYPOINT ["./dockerentry"]
CMD ["ash"]

