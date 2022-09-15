FROM quay.io/cloudhut/kowl

ENV PATH="/app:${PATH}"

COPY ./entrypoint.sh .

ENTRYPOINT ["/bin/sh", "entrypoint.sh"]