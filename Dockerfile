FROM python:3.8-slim-buster

RUN pip install ipython

# Not running as root.
ADD https://github.com/Yelp/dumb-init/releases/download/v1.2.0/dumb-init_1.2.0_amd64 /usr/local/bin/dumb-init
RUN chmod +x /usr/local/bin/dumb-init

WORKDIR /app

# Add user so we don't need --no-sandbox.
RUN groupadd -r sigflag && useradd -r -g sigflag -G audio,video sigflag \
    && mkdir -p /home/sigflag \
    && chown -R sigflag:sigflag .

USER sigflag
COPY filter.py .

ARG PORT
ARG REGEX
ENV PORT "${PORT}"
ENV REGEX "${REGEX}"
ARG FLAG

RUN echo ${FLAG} > flag.txt
EXPOSE ${PORT}
ENTRYPOINT ["dumb-init", "--"]
CMD python ./filter.py "${PORT}" "${REGEX}"