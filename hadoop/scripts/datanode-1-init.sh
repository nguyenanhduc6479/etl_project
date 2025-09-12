#!/usr/bin/env bash
set -euo pipefail
export HADOOP_HOME=/opt/hadoop
export HADOOP_CONF_DIR=${HADOOP_CONF_DIR:-$HADOOP_HOME/etc/hadoop}

ensure_log4j() {
  local target="$HADOOP_CONF_DIR/log4j.properties"
  local alt_dir="/opt/hadoop/logconf"
  local alt="$alt_dir/log4j.properties"

  if [ -f "$target" ]; then
    echo "[DN] Found $target"
    return
  fi

  echo "[DN] log4j.properties missing -> creating default..."
  mkdir -p "$alt_dir"
  cat > "$alt" <<'EOF'
log4j.rootLogger=INFO, console
log4j.appender.console=org.apache.log4j.ConsoleAppender
log4j.appender.console.target=System.out
log4j.appender.console.layout=org.apache.log4j.PatternLayout
log4j.appender.console.layout.ConversionPattern=%d{ISO8601} %p %c: %m%n
EOF

  if [ -w "$HADOOP_CONF_DIR" ]; then
    cp -f "$alt" "$target"
  else
    export HADOOP_OPTS="${HADOOP_OPTS:-} -Dlog4j.configuration=file:$alt"
  fi
}

wait_for_namenode() {
  local host="${HDFS_NAMENODE_HOST:-hdfs-namenode}"
  local port="${HDFS_NAMENODE_PORT:-9000}"
  local retries=60
  echo "[DN] Waiting for NameNode $host:$port ..."
  for i in $(seq 1 "$retries"); do
    if (exec 3<>"/dev/tcp/$host/$port") >/dev/null 2>&1; then
      exec 3>&- 3<&-
      echo "[DN] NameNode is up."
      return 0
    fi
    sleep 2
  done
  echo "[DN] ERROR: NameNode not reachable" >&2
  return 1
}

ensure_log4j
mkdir -p /hadoop/dfs/data
wait_for_namenode
exec "$HADOOP_HOME/bin/hdfs" datanode
