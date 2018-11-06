graph [
  node [
    id 0
    label "test"
    ip "10.1.0.1"
  ]
  node [
    id 1
    label "test1"
    ip "10.1.0.2"
  ]
  node [
    id 2
    label "test3"
    ip "10.1.0.3"
  ]
  node [
    id 3
    label "test2"
    ip "10.1.0.4"
  ]
  node [
    id 4
    label "test4"
    ip "10.1.0.5"
  ]
  edge [
    source 0
    target 1
  ]
  edge [
    source 0
    target 2
  ]
  edge [
    source 2
    target 3
  ]
  edge [
    source 2
    target 4
  ]
]
