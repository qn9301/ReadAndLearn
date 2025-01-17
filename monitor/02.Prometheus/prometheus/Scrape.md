

Scrape_path

 



prometheus\prometheus\config\testdata\conf.good.yml


E:\workspace\go\prometheus\prometheus\vendor\github.com\
prometheus\prometheus\config\testdata\conf.good.yml


# my global config
global:
  scrape_interval:     15s
  evaluation_interval: 30s
  # scrape_timeout is set to the global default (10s).

  external_labels:
    monitor: codelab
    foo:     bar

rule_files:
- "first.rules"
- "/absolute/second.rules"
- "my/*.rules"

remote_write:
  - url: http://remote1/push
    write_relabel_configs:
    - source_labels: [__name__]
      regex:         expensive.*
      action:        drop
  - url: http://remote2/push

scrape_configs:
- job_name: prometheus

  honor_labels: true
  # scrape_interval is defined by the configured global (15s).
  # scrape_timeout is defined by the global default (10s).

  # metrics_path defaults to '/metrics'
  # scheme defaults to 'http'.

  file_sd_configs:
    - files:
      - foo/*.slow.json
      - foo/*.slow.yml
      - single/file.yml
      refresh_interval: 10m
    - files:
      - bar/*.yaml

  static_configs:
  - targets: ['localhost:9090', 'localhost:9191']
    labels:
      my:   label
      your: label

  relabel_configs:
  - source_labels: [job, __meta_dns_name]
    regex:         (.*)some-[regex]
    target_label:  job
    replacement:   foo-${1}
    # action defaults to 'replace'
  - source_labels: [abc]
    target_label:  cde
  - replacement:   static
    target_label:  abc
  - regex:
    replacement:   static
    target_label:  abc

  bearer_token_file: valid_token_file


- job_name: service-x

  basic_auth:
    username: admin_name
    password: admin_password

  scrape_interval: 50s
  scrape_timeout:  5s

  sample_limit: 1000

  metrics_path: /my_path
  scheme: https

  dns_sd_configs:
  - refresh_interval: 15s
    names:
    - first.dns.address.domain.com
    - second.dns.address.domain.com
  - names:
    - first.dns.address.domain.com
    # refresh_interval defaults to 30s.

  relabel_configs:
  - source_labels: [job]
    regex:         (.*)some-[regex]
    action:        drop
  - source_labels: [__address__]
    modulus:       8
    target_label:  __tmp_hash
    action:        hashmod
  - source_labels: [__tmp_hash]
    regex:         1
    action:        keep
  - action:        labelmap
    regex:         1
  - action:        labeldrop
    regex:         d
  - action:        labelkeep
    regex:         k

  metric_relabel_configs:
  - source_labels: [__name__]
    regex:         expensive_metric.*
    action:        drop

- job_name: service-y

  consul_sd_configs:
  - server: 'localhost:1234'
    services: ['nginx', 'cache', 'mysql']
    scheme: https
    tls_config:
      ca_file: valid_ca_file
      cert_file: valid_cert_file
      key_file:  valid_key_file
      insecure_skip_verify: false

  relabel_configs:
  - source_labels: [__meta_sd_consul_tags]
    separator:     ','
    regex:         label:([^=]+)=([^,]+)
    target_label:  ${1}
    replacement:   ${2}

- job_name: service-z

  tls_config:
    cert_file: valid_cert_file
    key_file: valid_key_file

  bearer_token: avalidtoken

- job_name: service-kubernetes

  kubernetes_sd_configs:
  - role: endpoints
    api_server: 'https://localhost:1234'

    basic_auth:
      username: 'myusername'
      password: 'mypassword'

- job_name: service-marathon
  marathon_sd_configs:
  - servers:
    - 'https://marathon.example.com:443'

    tls_config:
      cert_file: valid_cert_file
      key_file: valid_key_file

- job_name: service-ec2
  ec2_sd_configs:
    - region: us-east-1
      access_key: access
      secret_key: secret
      profile: profile

- job_name: service-azure
  azure_sd_configs:
    - subscription_id: 11AAAA11-A11A-111A-A111-1111A1111A11
      tenant_id: BBBB222B-B2B2-2B22-B222-2BB2222BB2B2
      client_id: 333333CC-3C33-3333-CCC3-33C3CCCCC33C
      client_secret: nAdvAK2oBuVym4IXix
      port: 9100

- job_name: service-nerve
  nerve_sd_configs:
    - servers:
      - localhost
      paths:
      - /monitoring

- job_name: 0123service-xxx
  metrics_path: /metrics
  static_configs:
    - targets:
      - localhost:9090

- job_name: 測試
  metrics_path: /metrics
  static_configs:
    - targets:
      - localhost:9090

- job_name: service-triton
  triton_sd_configs:
  - account: 'testAccount'
    dns_suffix: 'triton.example.com'
    endpoint: 'triton.example.com'
    port: 9163
    refresh_interval: 1m
    version: 1
    tls_config:
      cert_file: testdata/valid_cert_file
      key_file: testdata/valid_key_file

alerting:
  alertmanagers:
  - scheme: https
    static_configs:
    - targets:
      - "1.2.3.4:9093"
      - "1.2.3.5:9093"
      - "1.2.3.6:9093"



