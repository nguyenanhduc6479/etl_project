#!/usr/bin/env bash
set -euo pipefail

export HADOOP_HOME=/opt/hadoop
export HADOOP_CONF_DIR=${HADOOP_CONF_DIR:-$HADOOP_HOME/etc/hadoop}

ensure_log4j() {
  local target="$HADOOP_CONF_DIR/log4j.properties"
  local alt_dir="/opt/hadoop/logconf"
  local alt="$alt_dir/log4j.properties"

  if [ -f "$target" ]; then
    echo "[NN] Found $target"
    return
  fi

  echo "[NN] log4j.properties missing -> creating default..."
  mkdir -p "$alt_dir"

  cat > "$alt" <<'EOF'
log4j.rootLogger=INFO, console
log4j.appender.console=org.apache.log4j.ConsoleAppender
log4j.appender.console.target=System.out
log4j.appender.console.layout=org.apache.log4j.PatternLayout
log4j.appender.console.layout.ConversionPattern=%d{ISO8601} %p %c: %m%n
EOF

  if [ -w "$HADOOP_CONF_DIR" ]; then
    # conf không read-only -> copy vào đúng chỗ Hadoop mong đợi
    cp -f "$alt" "$target"
  else
    # conf read-only -> trỏ Hadoop tới file thay thế
    export HADOOP_OPTS="${HADOOP_OPTS:-} -Dlog4j.configuration=file:$alt"
  fi
}

# --- tạo file log4j nếu thiếu
ensure_log4j

# --- NameNode storage & start
mkdir -p /hadoop/dfs/name
if [ ! -d "/hadoop/dfs/name/current" ]; then
  echo "[NN] First run -> format namenode"
  $HADOOP_HOME/bin/hdfs namenode -format -nonInteractive -force
fi

# chạy foreground để container không thoát
exec $HADOOP_HOME/bin/hdfs namenode
