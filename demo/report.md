# API Archaeologist inferred reference

INFERRED, NOT VERIFIED. Schema is inferred from synthetic fixtures; unknowns are marked, not filled in.

All input records explicitly labelled synthetic: True. The synthetic-fixture banner describes the bundled demonstration; other input provenance is unverified.

## Endpoint catalogue

All entries are inferred observations, never confirmed contracts.

### GET /inventory

Confidence: medium: repeated observations; not verified

Evidence: [ev-8495457c264eaa6b](#ev-8495457c264eaa6b), [ev-f54bfa7fa8030ae2](#ev-f54bfa7fa8030ae2)

Unknown: auth necessity, unobserved behavior, and query necessity.

```json
{
  "auth": [
    {
      "confidence": "medium: repeated observations; not verified",
      "evidence_ids": [
        "ev-8495457c264eaa6b",
        "ev-f54bfa7fa8030ae2"
      ],
      "value": {
        "header": "authorization",
        "required": "unknown",
        "scheme": "bearer"
      }
    }
  ],
  "evidence_ids": [
    "ev-8495457c264eaa6b",
    "ev-f54bfa7fa8030ae2"
  ],
  "method": {
    "confidence": "medium: repeated observations; not verified",
    "evidence_ids": [
      "ev-8495457c264eaa6b",
      "ev-f54bfa7fa8030ae2"
    ],
    "value": "GET"
  },
  "path": {
    "confidence": "medium: repeated observations; not verified",
    "evidence_ids": [
      "ev-8495457c264eaa6b",
      "ev-f54bfa7fa8030ae2"
    ],
    "value": "/inventory"
  },
  "path_parameters": {},
  "query_parameters": {},
  "request_shape": {
    "confidence": "unknown: no observed body",
    "evidence_ids": [
      "ev-8495457c264eaa6b",
      "ev-f54bfa7fa8030ae2"
    ],
    "value": "unknown"
  },
  "responses": {
    "200": {
      "shape": {
        "confidence": "conflicting: no merged contract",
        "evidence_ids": [
          "ev-8495457c264eaa6b",
          "ev-f54bfa7fa8030ae2"
        ],
        "value": {
          "state": "conflicting",
          "variants": [
            {
              "confidence": "conflicting: incompatible observed types",
              "evidence_ids": [
                "ev-f54bfa7fa8030ae2"
              ],
              "value": {
                "fields": {
                  "available": {
                    "type": "boolean"
                  }
                },
                "type": "object"
              }
            },
            {
              "confidence": "conflicting: incompatible observed types",
              "evidence_ids": [
                "ev-8495457c264eaa6b"
              ],
              "value": {
                "fields": {
                  "available": {
                    "type": "string"
                  }
                },
                "type": "object"
              }
            }
          ]
        }
      },
      "status": {
        "confidence": "medium: repeated observations; not verified",
        "evidence_ids": [
          "ev-8495457c264eaa6b",
          "ev-f54bfa7fa8030ae2"
        ],
        "value": 200
      }
    }
  }
}
```

### GET /orders

Confidence: medium: repeated observations; not verified

Evidence: [ev-2c4ebea7f0e6687c](#ev-2c4ebea7f0e6687c), [ev-7ad876f478cf8e8d](#ev-7ad876f478cf8e8d)

Unknown: auth necessity, unobserved behavior, and query necessity.

```json
{
  "auth": [
    {
      "confidence": "medium: repeated observations; not verified",
      "evidence_ids": [
        "ev-2c4ebea7f0e6687c",
        "ev-7ad876f478cf8e8d"
      ],
      "value": {
        "header": "authorization",
        "required": "unknown",
        "scheme": "bearer"
      }
    }
  ],
  "evidence_ids": [
    "ev-2c4ebea7f0e6687c",
    "ev-7ad876f478cf8e8d"
  ],
  "method": {
    "confidence": "medium: repeated observations; not verified",
    "evidence_ids": [
      "ev-2c4ebea7f0e6687c",
      "ev-7ad876f478cf8e8d"
    ],
    "value": "GET"
  },
  "path": {
    "confidence": "medium: repeated observations; not verified",
    "evidence_ids": [
      "ev-2c4ebea7f0e6687c",
      "ev-7ad876f478cf8e8d"
    ],
    "value": "/orders"
  },
  "path_parameters": {},
  "query_parameters": {
    "include_archived": {
      "confidence": "low: one observation",
      "evidence_ids": [
        "ev-2c4ebea7f0e6687c"
      ],
      "required": {
        "confidence": "unknown: observations cannot establish query necessity",
        "evidence_ids": [
          "ev-2c4ebea7f0e6687c",
          "ev-7ad876f478cf8e8d"
        ],
        "value": "unknown"
      },
      "value": [
        "string"
      ]
    }
  },
  "request_shape": {
    "confidence": "unknown: no observed body",
    "evidence_ids": [
      "ev-2c4ebea7f0e6687c",
      "ev-7ad876f478cf8e8d"
    ],
    "value": "unknown"
  },
  "responses": {
    "200": {
      "shape": {
        "confidence": "medium: repeated observations; not verified",
        "evidence_ids": [
          "ev-2c4ebea7f0e6687c",
          "ev-7ad876f478cf8e8d"
        ],
        "value": {
          "fields": {
            "orders": {
              "confidence": "medium: repeated observations; not verified",
              "evidence_ids": [
                "ev-2c4ebea7f0e6687c",
                "ev-7ad876f478cf8e8d"
              ],
              "required": {
                "confidence": "observed in 2/2 samples; inferred only",
                "evidence_ids": [
                  "ev-2c4ebea7f0e6687c",
                  "ev-7ad876f478cf8e8d"
                ],
                "value": true
              },
              "value": {
                "items": {
                  "confidence": "medium: repeated observations; not verified",
                  "evidence_ids": [
                    "ev-2c4ebea7f0e6687c",
                    "ev-7ad876f478cf8e8d"
                  ],
                  "value": {
                    "fields": {
                      "id": {
                        "confidence": "medium: repeated observations; not verified",
                        "evidence_ids": [
                          "ev-2c4ebea7f0e6687c",
                          "ev-7ad876f478cf8e8d"
                        ],
                        "required": {
                          "confidence": "observed in 2/2 samples; inferred only",
                          "evidence_ids": [
                            "ev-2c4ebea7f0e6687c",
                            "ev-7ad876f478cf8e8d"
                          ],
                          "value": true
                        },
                        "value": {
                          "type": "integer"
                        }
                      }
                    },
                    "type": "object"
                  }
                },
                "type": "array"
              }
            }
          },
          "type": "object"
        }
      },
      "status": {
        "confidence": "medium: repeated observations; not verified",
        "evidence_ids": [
          "ev-2c4ebea7f0e6687c",
          "ev-7ad876f478cf8e8d"
        ],
        "value": 200
      }
    }
  }
}
```

### GET /orders/{param_2}

Confidence: medium: repeated observations; not verified

Evidence: [ev-4ad744c73477a194](#ev-4ad744c73477a194), [ev-62536776afb6e0f1](#ev-62536776afb6e0f1), [ev-cd3277efe255bfa4](#ev-cd3277efe255bfa4), [ev-efaf5bfe926a2350](#ev-efaf5bfe926a2350)

Unknown: auth necessity, unobserved behavior, and query necessity.

```json
{
  "auth": [
    {
      "confidence": "medium: repeated observations; not verified",
      "evidence_ids": [
        "ev-62536776afb6e0f1",
        "ev-cd3277efe255bfa4",
        "ev-efaf5bfe926a2350"
      ],
      "value": {
        "header": "authorization",
        "required": "unknown",
        "scheme": "bearer"
      }
    }
  ],
  "evidence_ids": [
    "ev-4ad744c73477a194",
    "ev-62536776afb6e0f1",
    "ev-cd3277efe255bfa4",
    "ev-efaf5bfe926a2350"
  ],
  "method": {
    "confidence": "medium: repeated observations; not verified",
    "evidence_ids": [
      "ev-4ad744c73477a194",
      "ev-62536776afb6e0f1",
      "ev-cd3277efe255bfa4",
      "ev-efaf5bfe926a2350"
    ],
    "value": "GET"
  },
  "path": {
    "confidence": "medium: repeated observations; not verified",
    "evidence_ids": [
      "ev-4ad744c73477a194",
      "ev-62536776afb6e0f1",
      "ev-cd3277efe255bfa4",
      "ev-efaf5bfe926a2350"
    ],
    "value": "/orders/{param_2}"
  },
  "path_parameters": {
    "param_2": {
      "confidence": "medium: repeated observations; not verified",
      "evidence_ids": [
        "ev-4ad744c73477a194",
        "ev-62536776afb6e0f1",
        "ev-cd3277efe255bfa4",
        "ev-efaf5bfe926a2350"
      ],
      "value": [
        "integer"
      ]
    }
  },
  "query_parameters": {},
  "request_shape": {
    "confidence": "unknown: no observed body",
    "evidence_ids": [
      "ev-4ad744c73477a194",
      "ev-62536776afb6e0f1",
      "ev-cd3277efe255bfa4",
      "ev-efaf5bfe926a2350"
    ],
    "value": "unknown"
  },
  "responses": {
    "200": {
      "shape": {
        "confidence": "medium: repeated observations; not verified",
        "evidence_ids": [
          "ev-62536776afb6e0f1",
          "ev-cd3277efe255bfa4"
        ],
        "value": {
          "fields": {
            "id": {
              "confidence": "medium: repeated observations; not verified",
              "evidence_ids": [
                "ev-62536776afb6e0f1",
                "ev-cd3277efe255bfa4"
              ],
              "required": {
                "confidence": "observed in 2/2 samples; inferred only",
                "evidence_ids": [
                  "ev-62536776afb6e0f1",
                  "ev-cd3277efe255bfa4"
                ],
                "value": true
              },
              "value": {
                "type": "integer"
              }
            },
            "note": {
              "confidence": "low: one observation",
              "evidence_ids": [
                "ev-62536776afb6e0f1"
              ],
              "required": {
                "confidence": "observed in 1/2 samples; inferred only",
                "evidence_ids": [
                  "ev-62536776afb6e0f1",
                  "ev-cd3277efe255bfa4"
                ],
                "value": false
              },
              "value": {
                "type": "string"
              }
            },
            "total": {
              "confidence": "medium: repeated observations; not verified",
              "evidence_ids": [
                "ev-62536776afb6e0f1",
                "ev-cd3277efe255bfa4"
              ],
              "required": {
                "confidence": "observed in 2/2 samples; inferred only",
                "evidence_ids": [
                  "ev-62536776afb6e0f1",
                  "ev-cd3277efe255bfa4"
                ],
                "value": true
              },
              "value": {
                "type": "integer"
              }
            }
          },
          "type": "object"
        }
      },
      "status": {
        "confidence": "medium: repeated observations; not verified",
        "evidence_ids": [
          "ev-62536776afb6e0f1",
          "ev-cd3277efe255bfa4"
        ],
        "value": 200
      }
    },
    "404": {
      "shape": {
        "confidence": "low: one observation",
        "evidence_ids": [
          "ev-efaf5bfe926a2350"
        ],
        "value": {
          "fields": {
            "error": {
              "confidence": "low: one observation",
              "evidence_ids": [
                "ev-efaf5bfe926a2350"
              ],
              "required": {
                "confidence": "observed in 1/1 samples; inferred only",
                "evidence_ids": [
                  "ev-efaf5bfe926a2350"
                ],
                "value": true
              },
              "value": {
                "type": "string"
              }
            }
          },
          "type": "object"
        }
      },
      "status": {
        "confidence": "low: one observation",
        "evidence_ids": [
          "ev-efaf5bfe926a2350"
        ],
        "value": 404
      }
    }
  }
}
```

### POST /orders

Confidence: medium: repeated observations; not verified

Evidence: [ev-7b297c1511b022ea](#ev-7b297c1511b022ea), [ev-def27801e0719916](#ev-def27801e0719916)

Unknown: auth necessity, unobserved behavior, and query necessity.

```json
{
  "auth": [
    {
      "confidence": "low: one observation",
      "evidence_ids": [
        "ev-def27801e0719916"
      ],
      "value": {
        "header": "authorization",
        "required": "unknown",
        "scheme": "bearer"
      }
    }
  ],
  "evidence_ids": [
    "ev-7b297c1511b022ea",
    "ev-def27801e0719916"
  ],
  "method": {
    "confidence": "medium: repeated observations; not verified",
    "evidence_ids": [
      "ev-7b297c1511b022ea",
      "ev-def27801e0719916"
    ],
    "value": "POST"
  },
  "path": {
    "confidence": "medium: repeated observations; not verified",
    "evidence_ids": [
      "ev-7b297c1511b022ea",
      "ev-def27801e0719916"
    ],
    "value": "/orders"
  },
  "path_parameters": {},
  "query_parameters": {},
  "request_shape": {
    "confidence": "medium: repeated observations; not verified",
    "evidence_ids": [
      "ev-7b297c1511b022ea",
      "ev-def27801e0719916"
    ],
    "value": {
      "fields": {
        "quantity": {
          "confidence": "medium: repeated observations; not verified",
          "evidence_ids": [
            "ev-7b297c1511b022ea",
            "ev-def27801e0719916"
          ],
          "required": {
            "confidence": "observed in 2/2 samples; inferred only",
            "evidence_ids": [
              "ev-7b297c1511b022ea",
              "ev-def27801e0719916"
            ],
            "value": true
          },
          "value": {
            "type": "integer"
          }
        },
        "sku": {
          "confidence": "medium: repeated observations; not verified",
          "evidence_ids": [
            "ev-7b297c1511b022ea",
            "ev-def27801e0719916"
          ],
          "required": {
            "confidence": "observed in 2/2 samples; inferred only",
            "evidence_ids": [
              "ev-7b297c1511b022ea",
              "ev-def27801e0719916"
            ],
            "value": true
          },
          "value": {
            "type": "string"
          }
        }
      },
      "type": "object"
    }
  },
  "responses": {
    "201": {
      "shape": {
        "confidence": "low: one observation",
        "evidence_ids": [
          "ev-def27801e0719916"
        ],
        "value": {
          "fields": {
            "id": {
              "confidence": "low: one observation",
              "evidence_ids": [
                "ev-def27801e0719916"
              ],
              "required": {
                "confidence": "observed in 1/1 samples; inferred only",
                "evidence_ids": [
                  "ev-def27801e0719916"
                ],
                "value": true
              },
              "value": {
                "type": "integer"
              }
            }
          },
          "type": "object"
        }
      },
      "status": {
        "confidence": "low: one observation",
        "evidence_ids": [
          "ev-def27801e0719916"
        ],
        "value": 201
      }
    }
  }
}
```

## Conflict list

```json
[
  {
    "endpoint": "GET /inventory",
    "evidence_ids": [
      "ev-8495457c264eaa6b",
      "ev-f54bfa7fa8030ae2"
    ],
    "location": "response.200",
    "variants": [
      {
        "confidence": "conflicting: incompatible observed types",
        "evidence_ids": [
          "ev-f54bfa7fa8030ae2"
        ],
        "value": {
          "fields": {
            "available": {
              "type": "boolean"
            }
          },
          "type": "object"
        }
      },
      {
        "confidence": "conflicting: incompatible observed types",
        "evidence_ids": [
          "ev-8495457c264eaa6b"
        ],
        "value": {
          "fields": {
            "available": {
              "type": "string"
            }
          },
          "type": "object"
        }
      }
    ]
  }
]
```

## Unknown list

```json
[
  {
    "endpoint": "GET /inventory",
    "evidence_ids": [
      "ev-8495457c264eaa6b",
      "ev-f54bfa7fa8030ae2"
    ],
    "location": "request",
    "reason": "no observed body"
  },
  {
    "endpoint": "GET /inventory",
    "evidence_ids": [
      "ev-8495457c264eaa6b",
      "ev-f54bfa7fa8030ae2"
    ],
    "location": "auth_requirement",
    "reason": "observed headers do not prove authentication requirements"
  },
  {
    "endpoint": "GET /inventory",
    "evidence_ids": [
      "ev-8495457c264eaa6b",
      "ev-f54bfa7fa8030ae2"
    ],
    "location": "unobserved_behavior",
    "reason": "unseen statuses, fields, and endpoints are unknown"
  },
  {
    "endpoint": "GET /orders",
    "evidence_ids": [
      "ev-2c4ebea7f0e6687c",
      "ev-7ad876f478cf8e8d"
    ],
    "location": "query.include_archived.required",
    "reason": "observations cannot establish query necessity"
  },
  {
    "endpoint": "GET /orders",
    "evidence_ids": [
      "ev-2c4ebea7f0e6687c",
      "ev-7ad876f478cf8e8d"
    ],
    "location": "request",
    "reason": "no observed body"
  },
  {
    "endpoint": "GET /orders",
    "evidence_ids": [
      "ev-2c4ebea7f0e6687c",
      "ev-7ad876f478cf8e8d"
    ],
    "location": "auth_requirement",
    "reason": "observed headers do not prove authentication requirements"
  },
  {
    "endpoint": "GET /orders",
    "evidence_ids": [
      "ev-2c4ebea7f0e6687c",
      "ev-7ad876f478cf8e8d"
    ],
    "location": "unobserved_behavior",
    "reason": "unseen statuses, fields, and endpoints are unknown"
  },
  {
    "endpoint": "GET /orders/{param_2}",
    "evidence_ids": [
      "ev-4ad744c73477a194",
      "ev-62536776afb6e0f1",
      "ev-cd3277efe255bfa4",
      "ev-efaf5bfe926a2350"
    ],
    "location": "request",
    "reason": "no observed body"
  },
  {
    "endpoint": "GET /orders/{param_2}",
    "evidence_ids": [
      "ev-4ad744c73477a194",
      "ev-62536776afb6e0f1",
      "ev-cd3277efe255bfa4",
      "ev-efaf5bfe926a2350"
    ],
    "location": "auth_requirement",
    "reason": "observed headers do not prove authentication requirements"
  },
  {
    "endpoint": "GET /orders/{param_2}",
    "evidence_ids": [
      "ev-4ad744c73477a194",
      "ev-62536776afb6e0f1",
      "ev-cd3277efe255bfa4",
      "ev-efaf5bfe926a2350"
    ],
    "location": "unobserved_behavior",
    "reason": "unseen statuses, fields, and endpoints are unknown"
  },
  {
    "endpoint": "POST /orders",
    "evidence_ids": [
      "ev-7b297c1511b022ea",
      "ev-def27801e0719916"
    ],
    "location": "auth_requirement",
    "reason": "observed headers do not prove authentication requirements"
  },
  {
    "endpoint": "POST /orders",
    "evidence_ids": [
      "ev-7b297c1511b022ea",
      "ev-def27801e0719916"
    ],
    "location": "unobserved_behavior",
    "reason": "unseen statuses, fields, and endpoints are unknown"
  }
]
```

## Evidence catalogue

<a id="ev-efaf5bfe926a2350"></a>
### ev-efaf5bfe926a2350

Source: `errors.json#0`. Synthetic: True.

```json
{
  "id": "ev-efaf5bfe926a2350",
  "kind": "error",
  "request": {
    "body": null,
    "body_known": false,
    "headers": {
      "authorization": "Bearer fictional-token"
    },
    "method": "GET",
    "path": "/orders/999",
    "query": {}
  },
  "response": {
    "body": {
      "error": "fictional order missing"
    },
    "status": 404
  },
  "source": "errors.json#0",
  "synthetic": true
}
```

<a id="ev-4ad744c73477a194"></a>
### ev-4ad744c73477a194

Source: `examples.py#L3`. Synthetic: True.

```json
{
  "id": "ev-4ad744c73477a194",
  "kind": "code",
  "request": {
    "body": null,
    "body_known": false,
    "headers": {},
    "method": "GET",
    "path": "/orders/101",
    "query": {}
  },
  "response": null,
  "source": "examples.py#L3",
  "synthetic": true
}
```

<a id="ev-7b297c1511b022ea"></a>
### ev-7b297c1511b022ea

Source: `examples.py#L4`. Synthetic: True.

```json
{
  "id": "ev-7b297c1511b022ea",
  "kind": "code",
  "request": {
    "body": {
      "quantity": 1,
      "sku": "FICTIONAL-B"
    },
    "body_known": true,
    "headers": {},
    "method": "POST",
    "path": "/orders",
    "query": {}
  },
  "response": null,
  "source": "examples.py#L4",
  "synthetic": true
}
```

<a id="ev-62536776afb6e0f1"></a>
### ev-62536776afb6e0f1

Source: `traffic.json#0`. Synthetic: True.

```json
{
  "id": "ev-62536776afb6e0f1",
  "kind": "traffic",
  "request": {
    "body": null,
    "body_known": false,
    "headers": {
      "authorization": "Bearer fictional-token"
    },
    "method": "GET",
    "path": "/orders/101",
    "query": {}
  },
  "response": {
    "body": {
      "id": 101,
      "note": "gift",
      "total": 12
    },
    "status": 200
  },
  "source": "traffic.json#0",
  "synthetic": true
}
```

<a id="ev-cd3277efe255bfa4"></a>
### ev-cd3277efe255bfa4

Source: `traffic.json#1`. Synthetic: True.

```json
{
  "id": "ev-cd3277efe255bfa4",
  "kind": "traffic",
  "request": {
    "body": null,
    "body_known": false,
    "headers": {
      "authorization": "Bearer fictional-token"
    },
    "method": "GET",
    "path": "/orders/202",
    "query": {}
  },
  "response": {
    "body": {
      "id": 202,
      "total": 24
    },
    "status": 200
  },
  "source": "traffic.json#1",
  "synthetic": true
}
```

<a id="ev-2c4ebea7f0e6687c"></a>
### ev-2c4ebea7f0e6687c

Source: `traffic.json#2`. Synthetic: True.

```json
{
  "id": "ev-2c4ebea7f0e6687c",
  "kind": "traffic",
  "request": {
    "body": null,
    "body_known": false,
    "headers": {
      "authorization": "Bearer fictional-token"
    },
    "method": "GET",
    "path": "/orders",
    "query": {
      "include_archived": "true"
    }
  },
  "response": {
    "body": {
      "orders": [
        {
          "id": 101
        }
      ]
    },
    "status": 200
  },
  "source": "traffic.json#2",
  "synthetic": true
}
```

<a id="ev-7ad876f478cf8e8d"></a>
### ev-7ad876f478cf8e8d

Source: `traffic.json#3`. Synthetic: True.

```json
{
  "id": "ev-7ad876f478cf8e8d",
  "kind": "traffic",
  "request": {
    "body": null,
    "body_known": false,
    "headers": {
      "authorization": "Bearer fictional-token"
    },
    "method": "GET",
    "path": "/orders",
    "query": {}
  },
  "response": {
    "body": {
      "orders": [
        {
          "id": 202
        }
      ]
    },
    "status": 200
  },
  "source": "traffic.json#3",
  "synthetic": true
}
```

<a id="ev-def27801e0719916"></a>
### ev-def27801e0719916

Source: `traffic.json#4`. Synthetic: True.

```json
{
  "id": "ev-def27801e0719916",
  "kind": "traffic",
  "request": {
    "body": {
      "quantity": 2,
      "sku": "FICTIONAL-A"
    },
    "body_known": true,
    "headers": {
      "authorization": "Bearer fictional-token"
    },
    "method": "POST",
    "path": "/orders",
    "query": {}
  },
  "response": {
    "body": {
      "id": 303
    },
    "status": 201
  },
  "source": "traffic.json#4",
  "synthetic": true
}
```

<a id="ev-f54bfa7fa8030ae2"></a>
### ev-f54bfa7fa8030ae2

Source: `traffic.json#5`. Synthetic: True.

```json
{
  "id": "ev-f54bfa7fa8030ae2",
  "kind": "traffic",
  "request": {
    "body": null,
    "body_known": false,
    "headers": {
      "authorization": "Bearer fictional-token"
    },
    "method": "GET",
    "path": "/inventory",
    "query": {}
  },
  "response": {
    "body": {
      "available": true
    },
    "status": 200
  },
  "source": "traffic.json#5",
  "synthetic": true
}
```

<a id="ev-8495457c264eaa6b"></a>
### ev-8495457c264eaa6b

Source: `traffic.json#6`. Synthetic: True.

```json
{
  "id": "ev-8495457c264eaa6b",
  "kind": "traffic",
  "request": {
    "body": null,
    "body_known": false,
    "headers": {
      "authorization": "Bearer fictional-token"
    },
    "method": "GET",
    "path": "/inventory",
    "query": {}
  },
  "response": {
    "body": {
      "available": "unknown"
    },
    "status": 200
  },
  "source": "traffic.json#6",
  "synthetic": true
}
```
