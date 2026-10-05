const SOLICITANTES = [
    {
        nombre: "Juan Camilo Angel",
        descripcion: "Estable, todos los pagos → $4.5M",
        data: {
            id: "sol-001", status: "APPROVED",
            data: {
                fecha: "04/23/2026 04:58:50 PM",
                numero_identificacion_persona_natural: "70565593",
                primer_nombre_persona_natural: "JUAN CAMILO",
                primer_apellido_persona_natural: "ANGEL",
                aportantes: [{
                    tipo_identificacion_aportante_id: 2,
                    numero_identificacion_aportante: "901800001",
                    razon_social_aportante: "CONSTRUCTORA ANDES SAS",
                    tipo_cotizante_persona_natural: 1,
                    descripcion_cotizante_persona_natural: "Empleado",
                    tiene_novedad_retiro_actualmente_empleado: false,
                    tiene_licencia_no_remunerada_actualmente_empleador: false,
                    resultado_pagos: [
                        {ano_periodo_validado:2026,mes_periodo_validado:3,realizo_pago:true,ingresos:4500000},
                        {ano_periodo_validado:2026,mes_periodo_validado:2,realizo_pago:true,ingresos:4500000},
                        {ano_periodo_validado:2026,mes_periodo_validado:1,realizo_pago:true,ingresos:4500000},
                        {ano_periodo_validado:2025,mes_periodo_validado:12,realizo_pago:true,ingresos:4500000},
                        {ano_periodo_validado:2025,mes_periodo_validado:11,realizo_pago:true,ingresos:4500000},
                        {ano_periodo_validado:2025,mes_periodo_validado:10,realizo_pago:true,ingresos:4500000},
                        {ano_periodo_validado:2025,mes_periodo_validado:9,realizo_pago:true,ingresos:4500000},
                        {ano_periodo_validado:2025,mes_periodo_validado:8,realizo_pago:true,ingresos:4500000},
                        {ano_periodo_validado:2025,mes_periodo_validado:7,realizo_pago:true,ingresos:4500000},
                        {ano_periodo_validado:2025,mes_periodo_validado:6,realizo_pago:true,ingresos:4500000},
                        {ano_periodo_validado:2025,mes_periodo_validado:5,realizo_pago:true,ingresos:4500000},
                        {ano_periodo_validado:2025,mes_periodo_validado:4,realizo_pago:true,ingresos:4500000}
                    ]
                }]
            }
        }
    },
    {
        nombre: "Andrea Torres",
        descripcion: "Un mes sin pago intermedio (SI/NO/SI) → $2.8M",
        data: {
            id: "sol-002", status: "APPROVED",
            data: {
                fecha: "04/23/2026 05:05:00 PM",
                numero_identificacion_persona_natural: "52890002",
                primer_nombre_persona_natural: "ANDREA",
                primer_apellido_persona_natural: "TORRES",
                aportantes: [{
                    tipo_identificacion_aportante_id: 2,
                    numero_identificacion_aportante: "800200002",
                    razon_social_aportante: "ALIMENTOS DEL VALLE SA",
                    tipo_cotizante_persona_natural: 1,
                    descripcion_cotizante_persona_natural: "Empleado",
                    tiene_novedad_retiro_actualmente_empleado: false,
                    tiene_licencia_no_remunerada_actualmente_empleador: false,
                    resultado_pagos: [
                        {ano_periodo_validado:2026,mes_periodo_validado:3,realizo_pago:true,ingresos:2800000},
                        {ano_periodo_validado:2026,mes_periodo_validado:2,realizo_pago:false,ingresos:0},
                        {ano_periodo_validado:2026,mes_periodo_validado:1,realizo_pago:true,ingresos:2800000},
                        {ano_periodo_validado:2025,mes_periodo_validado:12,realizo_pago:true,ingresos:2800000},
                        {ano_periodo_validado:2025,mes_periodo_validado:11,realizo_pago:true,ingresos:2800000},
                        {ano_periodo_validado:2025,mes_periodo_validado:10,realizo_pago:true,ingresos:2800000},
                        {ano_periodo_validado:2025,mes_periodo_validado:9,realizo_pago:true,ingresos:2800000},
                        {ano_periodo_validado:2025,mes_periodo_validado:8,realizo_pago:true,ingresos:2800000},
                        {ano_periodo_validado:2025,mes_periodo_validado:7,realizo_pago:true,ingresos:2800000},
                        {ano_periodo_validado:2025,mes_periodo_validado:6,realizo_pago:true,ingresos:2800000},
                        {ano_periodo_validado:2025,mes_periodo_validado:5,realizo_pago:true,ingresos:2800000},
                        {ano_periodo_validado:2025,mes_periodo_validado:4,realizo_pago:true,ingresos:2800000}
                    ]
                }]
            }
        }
    },
    {
        nombre: "Roberto Silva",
        descripcion: "Pocos pagos recientes (NO/SI/SI) → $2.1M",
        data: {
            id: "sol-003", status: "APPROVED",
            data: {
                fecha: "04/23/2026 05:10:00 PM",
                numero_identificacion_persona_natural: "79345003",
                primer_nombre_persona_natural: "ROBERTO",
                primer_apellido_persona_natural: "SILVA",
                aportantes: [{
                    tipo_identificacion_aportante_id: 2,
                    numero_identificacion_aportante: "900300003",
                    razon_social_aportante: "LOGISTICA COLOMBIA LTDA",
                    tipo_cotizante_persona_natural: 1,
                    descripcion_cotizante_persona_natural: "Empleado",
                    tiene_novedad_retiro_actualmente_empleado: false,
                    tiene_licencia_no_remunerada_actualmente_empleador: false,
                    resultado_pagos: [
                        {ano_periodo_validado:2026,mes_periodo_validado:3,realizo_pago:true,ingresos:3200000},
                        {ano_periodo_validado:2026,mes_periodo_validado:2,realizo_pago:true,ingresos:3200000},
                        {ano_periodo_validado:2026,mes_periodo_validado:1,realizo_pago:false,ingresos:0},
                        {ano_periodo_validado:2025,mes_periodo_validado:12,realizo_pago:false,ingresos:0},
                        {ano_periodo_validado:2025,mes_periodo_validado:11,realizo_pago:true,ingresos:3200000},
                        {ano_periodo_validado:2025,mes_periodo_validado:10,realizo_pago:false,ingresos:0},
                        {ano_periodo_validado:2025,mes_periodo_validado:9,realizo_pago:true,ingresos:3200000},
                        {ano_periodo_validado:2025,mes_periodo_validado:8,realizo_pago:true,ingresos:3200000},
                        {ano_periodo_validado:2025,mes_periodo_validado:7,realizo_pago:false,ingresos:0},
                        {ano_periodo_validado:2025,mes_periodo_validado:6,realizo_pago:true,ingresos:3200000},
                        {ano_periodo_validado:2025,mes_periodo_validado:5,realizo_pago:false,ingresos:0},
                        {ano_periodo_validado:2025,mes_periodo_validado:4,realizo_pago:true,ingresos:3200000}
                    ]
                }]
            }
        }
    },
    {
        nombre: "Diana Castro",
        descripcion: "Dos meses sin pago, buen historial largo → $6.0M",
        data: {
            id: "sol-004", status: "APPROVED",
            data: {
                fecha: "04/23/2026 05:15:00 PM",
                numero_identificacion_persona_natural: "41567004",
                primer_nombre_persona_natural: "DIANA",
                primer_apellido_persona_natural: "CASTRO",
                aportantes: [{
                    tipo_identificacion_aportante_id: 2,
                    numero_identificacion_aportante: "901400004",
                    razon_social_aportante: "TECNOLOGIA GLOBAL SAS",
                    tipo_cotizante_persona_natural: 1,
                    descripcion_cotizante_persona_natural: "Empleado",
                    tiene_novedad_retiro_actualmente_empleado: false,
                    tiene_licencia_no_remunerada_actualmente_empleador: false,
                    resultado_pagos: [
                        {ano_periodo_validado:2026,mes_periodo_validado:3,realizo_pago:true,ingresos:6000000},
                        {ano_periodo_validado:2026,mes_periodo_validado:2,realizo_pago:false,ingresos:0},
                        {ano_periodo_validado:2026,mes_periodo_validado:1,realizo_pago:false,ingresos:0},
                        {ano_periodo_validado:2025,mes_periodo_validado:12,realizo_pago:true,ingresos:6000000},
                        {ano_periodo_validado:2025,mes_periodo_validado:11,realizo_pago:true,ingresos:6000000},
                        {ano_periodo_validado:2025,mes_periodo_validado:10,realizo_pago:true,ingresos:6000000},
                        {ano_periodo_validado:2025,mes_periodo_validado:9,realizo_pago:true,ingresos:6000000},
                        {ano_periodo_validado:2025,mes_periodo_validado:8,realizo_pago:true,ingresos:6000000},
                        {ano_periodo_validado:2025,mes_periodo_validado:7,realizo_pago:true,ingresos:6000000},
                        {ano_periodo_validado:2025,mes_periodo_validado:6,realizo_pago:true,ingresos:6000000},
                        {ano_periodo_validado:2025,mes_periodo_validado:5,realizo_pago:true,ingresos:6000000},
                        {ano_periodo_validado:2025,mes_periodo_validado:4,realizo_pago:true,ingresos:6000000}
                    ]
                }]
            }
        }
    },
    {
        nombre: "Luis Vargas",
        descripcion: "Último mes sin pago → Bloqueado ($0)",
        data: {
            id: "sol-005", status: "APPROVED",
            data: {
                fecha: "04/23/2026 05:20:00 PM",
                numero_identificacion_persona_natural: "80123005",
                primer_nombre_persona_natural: "LUIS",
                primer_apellido_persona_natural: "VARGAS",
                aportantes: [{
                    tipo_identificacion_aportante_id: 2,
                    numero_identificacion_aportante: "800500005",
                    razon_social_aportante: "SERVICIOS INTEGRADOS SA",
                    tipo_cotizante_persona_natural: 1,
                    descripcion_cotizante_persona_natural: "Empleado",
                    tiene_novedad_retiro_actualmente_empleado: false,
                    tiene_licencia_no_remunerada_actualmente_empleador: false,
                    resultado_pagos: [
                        {ano_periodo_validado:2026,mes_periodo_validado:3,realizo_pago:false,ingresos:0},
                        {ano_periodo_validado:2026,mes_periodo_validado:2,realizo_pago:true,ingresos:1800000},
                        {ano_periodo_validado:2026,mes_periodo_validado:1,realizo_pago:true,ingresos:1800000},
                        {ano_periodo_validado:2025,mes_periodo_validado:12,realizo_pago:true,ingresos:1800000},
                        {ano_periodo_validado:2025,mes_periodo_validado:11,realizo_pago:true,ingresos:1800000},
                        {ano_periodo_validado:2025,mes_periodo_validado:10,realizo_pago:true,ingresos:1800000},
                        {ano_periodo_validado:2025,mes_periodo_validado:9,realizo_pago:true,ingresos:1800000},
                        {ano_periodo_validado:2025,mes_periodo_validado:8,realizo_pago:true,ingresos:1800000},
                        {ano_periodo_validado:2025,mes_periodo_validado:7,realizo_pago:true,ingresos:1800000},
                        {ano_periodo_validado:2025,mes_periodo_validado:6,realizo_pago:true,ingresos:1800000},
                        {ano_periodo_validado:2025,mes_periodo_validado:5,realizo_pago:true,ingresos:1800000},
                        {ano_periodo_validado:2025,mes_periodo_validado:4,realizo_pago:true,ingresos:1800000}
                    ]
                }]
            }
        }
    },
    {
        nombre: "Patricia Herrera",
        descripcion: "Dos empleadores, uno con retiro → $4.5M",
        data: {
            id: "sol-006", status: "APPROVED",
            data: {
                fecha: "04/23/2026 05:25:00 PM",
                numero_identificacion_persona_natural: "39876006",
                primer_nombre_persona_natural: "PATRICIA",
                primer_apellido_persona_natural: "HERRERA",
                aportantes: [
                    {
                        tipo_identificacion_aportante_id: 2,
                        numero_identificacion_aportante: "900600006",
                        razon_social_aportante: "INVERSIONES XYZ SAS",
                        tipo_cotizante_persona_natural: 1,
                        descripcion_cotizante_persona_natural: "Empleado",
                        tiene_novedad_retiro_actualmente_empleado: true,
                        tiene_licencia_no_remunerada_actualmente_empleador: false,
                        resultado_pagos: [
                            {ano_periodo_validado:2026,mes_periodo_validado:3,realizo_pago:true,ingresos:3000000},
                            {ano_periodo_validado:2026,mes_periodo_validado:2,realizo_pago:true,ingresos:3000000},
                            {ano_periodo_validado:2026,mes_periodo_validado:1,realizo_pago:true,ingresos:3000000},
                            {ano_periodo_validado:2025,mes_periodo_validado:12,realizo_pago:true,ingresos:3000000},
                            {ano_periodo_validado:2025,mes_periodo_validado:11,realizo_pago:true,ingresos:3000000},
                            {ano_periodo_validado:2025,mes_periodo_validado:10,realizo_pago:true,ingresos:3000000},
                            {ano_periodo_validado:2025,mes_periodo_validado:9,realizo_pago:true,ingresos:3000000},
                            {ano_periodo_validado:2025,mes_periodo_validado:8,realizo_pago:true,ingresos:3000000},
                            {ano_periodo_validado:2025,mes_periodo_validado:7,realizo_pago:true,ingresos:3000000},
                            {ano_periodo_validado:2025,mes_periodo_validado:6,realizo_pago:true,ingresos:3000000},
                            {ano_periodo_validado:2025,mes_periodo_validado:5,realizo_pago:true,ingresos:3000000},
                            {ano_periodo_validado:2025,mes_periodo_validado:4,realizo_pago:true,ingresos:3000000}
                        ]
                    },
                    {
                        tipo_identificacion_aportante_id: 2,
                        numero_identificacion_aportante: "901600007",
                        razon_social_aportante: "CONSULTORES DEL CARIBE SAS",
                        tipo_cotizante_persona_natural: 1,
                        descripcion_cotizante_persona_natural: "Empleado",
                        tiene_novedad_retiro_actualmente_empleado: false,
                        tiene_licencia_no_remunerada_actualmente_empleador: false,
                        resultado_pagos: [
                            {ano_periodo_validado:2026,mes_periodo_validado:3,realizo_pago:true,ingresos:2500000},
                            {ano_periodo_validado:2026,mes_periodo_validado:2,realizo_pago:true,ingresos:2500000},
                            {ano_periodo_validado:2026,mes_periodo_validado:1,realizo_pago:true,ingresos:2500000},
                            {ano_periodo_validado:2025,mes_periodo_validado:12,realizo_pago:true,ingresos:2500000},
                            {ano_periodo_validado:2025,mes_periodo_validado:11,realizo_pago:true,ingresos:2500000},
                            {ano_periodo_validado:2025,mes_periodo_validado:10,realizo_pago:true,ingresos:2500000},
                            {ano_periodo_validado:2025,mes_periodo_validado:9,realizo_pago:true,ingresos:2500000},
                            {ano_periodo_validado:2025,mes_periodo_validado:8,realizo_pago:true,ingresos:2500000},
                            {ano_periodo_validado:2025,mes_periodo_validado:7,realizo_pago:true,ingresos:2500000},
                            {ano_periodo_validado:2025,mes_periodo_validado:6,realizo_pago:true,ingresos:2500000},
                            {ano_periodo_validado:2025,mes_periodo_validado:5,realizo_pago:true,ingresos:2500000},
                            {ano_periodo_validado:2025,mes_periodo_validado:4,realizo_pago:true,ingresos:2500000}
                        ]
                    }
                ]
            }
        }
    },
    {
        nombre: "Santiago Mora",
        descripcion: "Licencia no remunerada → Bloqueado ($0)",
        data: {
            id: "sol-007", status: "APPROVED",
            data: {
                fecha: "04/23/2026 05:30:00 PM",
                numero_identificacion_persona_natural: "1098765007",
                primer_nombre_persona_natural: "SANTIAGO",
                primer_apellido_persona_natural: "MORA",
                aportantes: [{
                    tipo_identificacion_aportante_id: 2,
                    numero_identificacion_aportante: "800700008",
                    razon_social_aportante: "MINERIA NACIONAL SA",
                    tipo_cotizante_persona_natural: 1,
                    descripcion_cotizante_persona_natural: "Empleado",
                    tiene_novedad_retiro_actualmente_empleado: false,
                    tiene_licencia_no_remunerada_actualmente_empleador: true,
                    resultado_pagos: [
                        {ano_periodo_validado:2026,mes_periodo_validado:3,realizo_pago:true,ingresos:4000000},
                        {ano_periodo_validado:2026,mes_periodo_validado:2,realizo_pago:true,ingresos:4000000},
                        {ano_periodo_validado:2026,mes_periodo_validado:1,realizo_pago:true,ingresos:4000000},
                        {ano_periodo_validado:2025,mes_periodo_validado:12,realizo_pago:true,ingresos:4000000},
                        {ano_periodo_validado:2025,mes_periodo_validado:11,realizo_pago:true,ingresos:4000000},
                        {ano_periodo_validado:2025,mes_periodo_validado:10,realizo_pago:true,ingresos:4000000},
                        {ano_periodo_validado:2025,mes_periodo_validado:9,realizo_pago:true,ingresos:4000000},
                        {ano_periodo_validado:2025,mes_periodo_validado:8,realizo_pago:true,ingresos:4000000},
                        {ano_periodo_validado:2025,mes_periodo_validado:7,realizo_pago:true,ingresos:4000000},
                        {ano_periodo_validado:2025,mes_periodo_validado:6,realizo_pago:true,ingresos:4000000},
                        {ano_periodo_validado:2025,mes_periodo_validado:5,realizo_pago:true,ingresos:4000000},
                        {ano_periodo_validado:2025,mes_periodo_validado:4,realizo_pago:true,ingresos:4000000}
                    ]
                }]
            }
        }
    },
    {
        nombre: "Valentina Reyes",
        descripcion: "Ingreso alto, perfil perfecto → $12.0M",
        data: {
            id: "sol-008", status: "APPROVED",
            data: {
                fecha: "04/23/2026 05:35:00 PM",
                numero_identificacion_persona_natural: "63210008",
                primer_nombre_persona_natural: "VALENTINA",
                primer_apellido_persona_natural: "REYES",
                aportantes: [{
                    tipo_identificacion_aportante_id: 2,
                    numero_identificacion_aportante: "901800009",
                    razon_social_aportante: "BANCO PRINCIPAL SA",
                    tipo_cotizante_persona_natural: 1,
                    descripcion_cotizante_persona_natural: "Empleado",
                    tiene_novedad_retiro_actualmente_empleado: false,
                    tiene_licencia_no_remunerada_actualmente_empleador: false,
                    resultado_pagos: [
                        {ano_periodo_validado:2026,mes_periodo_validado:3,realizo_pago:true,ingresos:12000000},
                        {ano_periodo_validado:2026,mes_periodo_validado:2,realizo_pago:true,ingresos:12000000},
                        {ano_periodo_validado:2026,mes_periodo_validado:1,realizo_pago:true,ingresos:12000000},
                        {ano_periodo_validado:2025,mes_periodo_validado:12,realizo_pago:true,ingresos:12000000},
                        {ano_periodo_validado:2025,mes_periodo_validado:11,realizo_pago:true,ingresos:12000000},
                        {ano_periodo_validado:2025,mes_periodo_validado:10,realizo_pago:true,ingresos:12000000},
                        {ano_periodo_validado:2025,mes_periodo_validado:9,realizo_pago:true,ingresos:12000000},
                        {ano_periodo_validado:2025,mes_periodo_validado:8,realizo_pago:true,ingresos:12000000},
                        {ano_periodo_validado:2025,mes_periodo_validado:7,realizo_pago:true,ingresos:12000000},
                        {ano_periodo_validado:2025,mes_periodo_validado:6,realizo_pago:true,ingresos:12000000},
                        {ano_periodo_validado:2025,mes_periodo_validado:5,realizo_pago:true,ingresos:12000000},
                        {ano_periodo_validado:2025,mes_periodo_validado:4,realizo_pago:true,ingresos:12000000}
                    ]
                }]
            }
        }
    },
    {
        nombre: "Fernando Gutiérrez",
        descripcion: "Independiente filtrado + empleador → $2.5M",
        data: {
            id: "sol-009", status: "APPROVED",
            data: {
                fecha: "04/23/2026 05:40:00 PM",
                numero_identificacion_persona_natural: "71543009",
                primer_nombre_persona_natural: "FERNANDO",
                primer_apellido_persona_natural: "GUTIERREZ",
                aportantes: [
                    {
                        tipo_identificacion_aportante_id: 2,
                        numero_identificacion_aportante: "71543009",
                        razon_social_aportante: "FERNANDO GUTIERREZ",
                        tipo_cotizante_persona_natural: 2,
                        descripcion_cotizante_persona_natural: "Independiente",
                        tiene_novedad_retiro_actualmente_empleado: false,
                        tiene_licencia_no_remunerada_actualmente_empleador: false,
                        resultado_pagos: [
                            {ano_periodo_validado:2026,mes_periodo_validado:3,realizo_pago:true,ingresos:5000000},
                            {ano_periodo_validado:2026,mes_periodo_validado:2,realizo_pago:true,ingresos:5000000},
                            {ano_periodo_validado:2026,mes_periodo_validado:1,realizo_pago:true,ingresos:5000000},
                            {ano_periodo_validado:2025,mes_periodo_validado:12,realizo_pago:true,ingresos:5000000},
                            {ano_periodo_validado:2025,mes_periodo_validado:11,realizo_pago:true,ingresos:5000000},
                            {ano_periodo_validado:2025,mes_periodo_validado:10,realizo_pago:true,ingresos:5000000},
                            {ano_periodo_validado:2025,mes_periodo_validado:9,realizo_pago:true,ingresos:5000000},
                            {ano_periodo_validado:2025,mes_periodo_validado:8,realizo_pago:true,ingresos:5000000},
                            {ano_periodo_validado:2025,mes_periodo_validado:7,realizo_pago:true,ingresos:5000000},
                            {ano_periodo_validado:2025,mes_periodo_validado:6,realizo_pago:true,ingresos:5000000},
                            {ano_periodo_validado:2025,mes_periodo_validado:5,realizo_pago:true,ingresos:5000000},
                            {ano_periodo_validado:2025,mes_periodo_validado:4,realizo_pago:true,ingresos:5000000}
                        ]
                    },
                    {
                        tipo_identificacion_aportante_id: 2,
                        numero_identificacion_aportante: "900900010",
                        razon_social_aportante: "IMPORTADORA CENTRAL SAS",
                        tipo_cotizante_persona_natural: 1,
                        descripcion_cotizante_persona_natural: "Empleado",
                        tiene_novedad_retiro_actualmente_empleado: false,
                        tiene_licencia_no_remunerada_actualmente_empleador: false,
                        resultado_pagos: [
                            {ano_periodo_validado:2026,mes_periodo_validado:3,realizo_pago:true,ingresos:2500000},
                            {ano_periodo_validado:2026,mes_periodo_validado:2,realizo_pago:true,ingresos:2500000},
                            {ano_periodo_validado:2026,mes_periodo_validado:1,realizo_pago:true,ingresos:2500000},
                            {ano_periodo_validado:2025,mes_periodo_validado:12,realizo_pago:true,ingresos:2500000},
                            {ano_periodo_validado:2025,mes_periodo_validado:11,realizo_pago:true,ingresos:2500000},
                            {ano_periodo_validado:2025,mes_periodo_validado:10,realizo_pago:true,ingresos:2500000},
                            {ano_periodo_validado:2025,mes_periodo_validado:9,realizo_pago:true,ingresos:2500000},
                            {ano_periodo_validado:2025,mes_periodo_validado:8,realizo_pago:true,ingresos:2500000},
                            {ano_periodo_validado:2025,mes_periodo_validado:7,realizo_pago:true,ingresos:2500000},
                            {ano_periodo_validado:2025,mes_periodo_validado:6,realizo_pago:true,ingresos:2500000},
                            {ano_periodo_validado:2025,mes_periodo_validado:5,realizo_pago:true,ingresos:2500000},
                            {ano_periodo_validado:2025,mes_periodo_validado:4,realizo_pago:true,ingresos:2500000}
                        ]
                    }
                ]
            }
        }
    },
    {
        nombre: "Camila Ospina",
        descripcion: "Pagos irregulares, historial débil → $500K",
        data: {
            id: "sol-010", status: "APPROVED",
            data: {
                fecha: "04/23/2026 05:45:00 PM",
                numero_identificacion_persona_natural: "1015430010",
                primer_nombre_persona_natural: "CAMILA",
                primer_apellido_persona_natural: "OSPINA",
                aportantes: [{
                    tipo_identificacion_aportante_id: 2,
                    numero_identificacion_aportante: "901000011",
                    razon_social_aportante: "DISTRIBUIDORA EXPRESS SAS",
                    tipo_cotizante_persona_natural: 1,
                    descripcion_cotizante_persona_natural: "Empleado",
                    tiene_novedad_retiro_actualmente_empleado: false,
                    tiene_licencia_no_remunerada_actualmente_empleador: false,
                    resultado_pagos: [
                        {ano_periodo_validado:2026,mes_periodo_validado:3,realizo_pago:true,ingresos:1500000},
                        {ano_periodo_validado:2026,mes_periodo_validado:2,realizo_pago:false,ingresos:0},
                        {ano_periodo_validado:2026,mes_periodo_validado:1,realizo_pago:false,ingresos:0},
                        {ano_periodo_validado:2025,mes_periodo_validado:12,realizo_pago:true,ingresos:1500000},
                        {ano_periodo_validado:2025,mes_periodo_validado:11,realizo_pago:false,ingresos:0},
                        {ano_periodo_validado:2025,mes_periodo_validado:10,realizo_pago:true,ingresos:1500000},
                        {ano_periodo_validado:2025,mes_periodo_validado:9,realizo_pago:false,ingresos:0},
                        {ano_periodo_validado:2025,mes_periodo_validado:8,realizo_pago:true,ingresos:1500000},
                        {ano_periodo_validado:2025,mes_periodo_validado:7,realizo_pago:false,ingresos:0},
                        {ano_periodo_validado:2025,mes_periodo_validado:6,realizo_pago:true,ingresos:1500000},
                        {ano_periodo_validado:2025,mes_periodo_validado:5,realizo_pago:false,ingresos:0},
                        {ano_periodo_validado:2025,mes_periodo_validado:4,realizo_pago:false,ingresos:0}
                    ]
                }]
            }
        }
    }
];

// Base Experian Demo (UAT): solo personas que responden los DOS informes,
// Valor Ingreso (respuesta_id 4) y HDC+ (código 13). Verificado en vivo el
// 2026-10-03. Es la base de pruebas de Experian: nombres, cédulas e
// información vienen enmascarados y no corresponden a personas reales.
// `nombre`, `score`, `obligaciones` (vigentes + cerradas) y `vigentes` vienen
// de HDC+; `aportantes` y `cotizante` de Valor Ingreso.
// `nombre_vi` aparece cuando Valor Ingreso devuelve otro nombre de pila para
// la misma cédula; el primer apellido coincide.
const EXPERIAN_DEMO = [
    // Formato ambiente demo Valor Ingreso (JJJ 20260914): 24 cédulas
    { nombre: "Ruben Dario Martinez Garzon", cedula: "15446987", apellido: "MARTINEZ", tipo: "CC", score: 816, obligaciones: 30, vigentes: 7, aportantes: 1, cotizante: "Empleado", nombre_vi: "Jose Luis Martinez Garzon" },
    { nombre: "Yolanda Tobon Tobon", cedula: "39193322", apellido: "TOBON", tipo: "CC", score: 804, obligaciones: 51, vigentes: 4, aportantes: 1, cotizante: "Empleado", nombre_vi: "Rosalba Tobon Tobon" },
    { nombre: "Jennifer Matilde Callejas Angarita", cedula: "1023003654", apellido: "CALLEJAS", tipo: "CC", score: 743, obligaciones: 163, vigentes: 14, aportantes: 1, cotizante: "Empleado", nombre_vi: "Mario Callejas Angarita" },
    { nombre: "Sandra Janneth Munoz Herreria", cedula: "6853544", apellido: "MUÑOZ", tipo: "CC", score: 662, obligaciones: 5, vigentes: 0, aportantes: 1, cotizante: "Empleado" },
    { nombre: "Eugenio Montoya Arboleda", cedula: "1017178557", apellido: "MONTOYA", tipo: "CC", score: 868, obligaciones: 19, vigentes: 6, aportantes: 1, cotizante: "Pensionado", nombre_vi: "Ofelia Montoya Arboleda" },
    { nombre: "Juan Carlos Muñoz de Ossa", cedula: "71278597", apellido: "MUÑOZ", tipo: "CC", score: 827, obligaciones: 21, vigentes: 5, aportantes: 1, cotizante: "Pensionado", nombre_vi: "Luis Alvaro Muñoz de Ossa" },
    { nombre: "Nicolas Anibal Zuluaga Osorio", cedula: "71117679", apellido: "ZULUAGA", tipo: "CC", score: 814, obligaciones: 44, vigentes: 8, aportantes: 1, cotizante: "Empleado" },
    { nombre: "Gilberto Florez Diaz", cedula: "19328060", apellido: "FLOREZ", tipo: "CC", score: 677, obligaciones: 5, vigentes: 3, aportantes: 1, cotizante: "Empleado" },
    { nombre: "Alex Acosta Mejia", cedula: "71765991", apellido: "ACOSTA", tipo: "CC", score: 588, obligaciones: 35, vigentes: 6, aportantes: 1, cotizante: "Empleado", nombre_vi: "Eliria del Socorro Acosta Mejia" },
    { nombre: "Hernan Dario Arias Tabares", cedula: "1040045649", apellido: "ARIAS", tipo: "CC", score: 791, obligaciones: 38, vigentes: 6, aportantes: 1, cotizante: "Empleado", nombre_vi: "Luz Dary Arias Tabares" },
    { nombre: "Nora Emilse Cardona Garcia", cedula: "43558013", apellido: "CARDONA", tipo: "CC", score: 776, obligaciones: 98, vigentes: 10, aportantes: 1, cotizante: "Empleado", nombre_vi: "Maria Teresa Cardona Garcia" },
    { nombre: "Johan Arley Vanegas Serna", cedula: "1128465811", apellido: "VANEGAS", tipo: "CC", score: 721, obligaciones: 119, vigentes: 6, aportantes: 1, cotizante: "Empleado", nombre_vi: "Victoria Vanegas Serna" },
    { nombre: "Orlando Garaviz Zabala", cedula: "16656581", apellido: "GARAVIZ", tipo: "CC", score: 827, obligaciones: 84, vigentes: 3, aportantes: 1, cotizante: "Pensionado", nombre_vi: "Maria Rocio Garaviz Zabala" },
    { nombre: "Jacob Cardenas Marin", cedula: "70300657", apellido: "CARDENAS", tipo: "CC", score: 870, obligaciones: 45, vigentes: 8, aportantes: 1, cotizante: "Empleado", nombre_vi: "Maria de los Angeles Cardenas Marin" },
    { nombre: "Ramon Antonio Vasquez Taborda", cedula: "3382927", apellido: "VASQUEZ", tipo: "CC", score: 870, obligaciones: 33, vigentes: 3, aportantes: 1, cotizante: "Pensionado", nombre_vi: "Hector Vidal Vasquez Taborda" },
    { nombre: "Jose Antonio Velasco Fontecha", cedula: "19452849", apellido: "VELASCO", tipo: "CC", score: 601, obligaciones: 34, vigentes: 4, aportantes: 1, cotizante: "Empleado" },
    { nombre: "Luis Carlos Pereira Perez", cedula: "1041258701", apellido: "PEREIRA", tipo: "CC", score: 729, obligaciones: 23, vigentes: 11, aportantes: 1, cotizante: "Empleado" },
    { nombre: "Reimond Jose Rojas Anibal", cedula: "12400430", apellido: "ROJAS", tipo: "CC", score: 575, obligaciones: 46, vigentes: 8, aportantes: 1, cotizante: "Empleado" },
    { nombre: "Gerardo de Jesus Sanchez Cano", cedula: "98541406", apellido: "SANCHEZ", tipo: "CC", score: 539, obligaciones: 59, vigentes: 7, aportantes: 1, cotizante: "Empleado", nombre_vi: "Alvaro Mauricio Sanchez Cano" },
    { nombre: "Gloria Elena Arango Perez", cedula: "42899581", apellido: "ARANGO", tipo: "CC", score: 640, obligaciones: 103, vigentes: 13, aportantes: 1, cotizante: "Empleado", nombre_vi: "Adriana Patricia Arango Perez" },
    { nombre: "Marta Cecilia Giraldo Loaiza", cedula: "66721558", apellido: "GIRALDO", tipo: "CC", score: 770, obligaciones: 75, vigentes: 18, aportantes: 1, cotizante: "Empleado" },
    { nombre: "Diogenes Manuel Hidalgo Rojas", cedula: "71672697", apellido: "HIDALGO", tipo: "CC", score: 597, obligaciones: 23, vigentes: 2, aportantes: 1, cotizante: "Empleado", nombre_vi: "Hernan de Jesus Hidalgo Rojas" },
    { nombre: "Dayron Cardona Osorio", cedula: "1017130968", apellido: "CARDONA", tipo: "CC", score: 756, obligaciones: 26, vigentes: 6, aportantes: 1, cotizante: "Empleado", nombre_vi: "Maria Luisa Cardona Osorio" },
    { nombre: "Jairo Antonio Ochoa Ospina", cedula: "15525560", apellido: "OCHOA", tipo: "CC", score: 870, obligaciones: 32, vigentes: 5, aportantes: 1, cotizante: "Empleado", nombre_vi: "Adriana Elicet Ochoa Ospina" },
    // Lista Experian del 2026-10-02: 15 cédulas
    { nombre: "Jhank Paulo Prada Herrada", cedula: "1075307496", apellido: "PRADA", tipo: "CC", score: 870, obligaciones: 31, vigentes: 8, aportantes: 1, cotizante: "Empleado", nombre_vi: "Raul Vicente Prada Cortes" },
    { nombre: "Juan Felipe Carvajal Pineda", cedula: "1003805261", apellido: "CARVAJAL", tipo: "CC", score: 928, obligaciones: 10, vigentes: 4, aportantes: 2, cotizante: "Independiente", nombre_vi: "Jose Manuel Carvajal Pinzon" },
    { nombre: "Juan Pablo Giron Murcia", cedula: "1003805317", apellido: "GIRON", tipo: "CC", score: 769, obligaciones: 8, vigentes: 4, aportantes: 3, cotizante: "Empleado", nombre_vi: "Virgilio Roberto Giron Diaz" },
    { nombre: "Jheyson Leandro Cardenas Cuellar", cedula: "1075220361", apellido: "CARDENAS", tipo: "CC", score: 909, obligaciones: 71, vigentes: 6, aportantes: 3, cotizante: "Pensionado", nombre_vi: "Gustavo Alonso Cardenas Zuluaga" },
    { nombre: "Sergio Daniel Cometa Trujillo", cedula: "1075314189", apellido: "COMETA", tipo: "CC", score: 792, obligaciones: 4, vigentes: 2, aportantes: 2, cotizante: "Empleado", nombre_vi: "Reiner Werner Cometa" },
    { nombre: "Oscar Alejandro Serrano Urueña", cedula: "1075315125", apellido: "SERRANO", tipo: "CC", score: 781, obligaciones: 22, vigentes: 7, aportantes: 3, cotizante: "Pensionado", nombre_vi: "Francisco Alberto Serrano Avila" },
    { nombre: "Cristian Alexander Garzon Florez", cedula: "1075317291", apellido: "GARZON", tipo: "CC", score: 831, obligaciones: 9, vigentes: 2, aportantes: 3, cotizante: "Empleado", nombre_vi: "Gilberto Mauricio Garzon Arias" },
    { nombre: "Mairon Alexis Murcia Villalba", cedula: "1075319008", apellido: "MURCIA", tipo: "CC", score: 844, obligaciones: 17, vigentes: 8, aportantes: 8, cotizante: "Pensionado", nombre_vi: "Hernan Javier Murcia Calderon" },
    { nombre: "Julian Camilo Pastrana Bravo", cedula: "1075319036", apellido: "PASTRANA", tipo: "CC", score: 921, obligaciones: 2, vigentes: 2, aportantes: 2, cotizante: "Empleado", nombre_vi: "Gabriel Pastrana Roldan" },
    { nombre: "David Alejandro Reyes Perez", cedula: "1076501150", apellido: "REYES", tipo: "CC", score: 699, obligaciones: 3, vigentes: 2, aportantes: 1, cotizante: "Empleado", nombre_vi: "Mario Alejandro Reyes Mahecha" },
    { nombre: "Andres Mauricio Penagos Gonzalez", cedula: "1080296993", apellido: "PENAGOS", tipo: "CC", score: 754, obligaciones: 7, vigentes: 3, aportantes: 2, cotizante: "Independiente", nombre_vi: "Orlando Penagos Duarte" },
    { nombre: "Harold Bello Valenzuela", cedula: "7690312", apellido: "BELLO", tipo: "CC", score: 837, obligaciones: 84, vigentes: 10, aportantes: 3, cotizante: "Empleado", nombre_vi: "Luis Hernando Bello Aldana" },
    { nombre: "Marco Fidel Valbuena Macias", cedula: "83243606", apellido: "VALBUENA", tipo: "CC", score: 844, obligaciones: 42, vigentes: 8, aportantes: 1, cotizante: "Empleado", nombre_vi: "Carlos Mauricio Valbuena Perez" },
    { nombre: "Katerin Lorena Silva Blanquiceth", cedula: "1003801196", apellido: "SILVA", tipo: "CC", score: 864, obligaciones: 34, vigentes: 9, aportantes: 2, cotizante: "Independiente", nombre_vi: "Juan Carlos Silva Perdomo" },
    { nombre: "Jader Mauricio Chalar Soto", cedula: "1075211751", apellido: "CHALAR", tipo: "CC", score: 909, obligaciones: 170, vigentes: 15, aportantes: 3, cotizante: "Empleado", nombre_vi: "Efrain Chalar Gonzalez" },
    // Base HDC+ inicial: 19 cédulas (ahora también con Valor Ingreso)
    { nombre: "Elisabet Valderrama Valderrama", cedula: "1128473987", apellido: "VALDERRAMA", tipo: "CC", score: 770, obligaciones: 14, vigentes: 5, aportantes: 2, cotizante: "Pensionado / Empleado" },
    { nombre: "Camilo Uribe Monsalve", cedula: "1017260977", apellido: "URIBE", tipo: "CC", score: 658, obligaciones: 11, vigentes: 5, aportantes: 2, cotizante: "Empleado" },
    { nombre: "Felix Sanchez Arellano", cedula: "1412942", apellido: "SANCHEZ", tipo: "CE", score: 0, obligaciones: 8, vigentes: 2, aportantes: 1, cotizante: "Empleado" },
    { nombre: "Darwin Ferney Vergara Angulo", cedula: "1003289970", apellido: "VERGARA", tipo: "CC", score: 482, obligaciones: 21, vigentes: 4, aportantes: 1, cotizante: "Pensionado" },
    { nombre: "Victor Alfonso Atehortua Osorio", cedula: "1001390631", apellido: "ATEHORTUA", tipo: "CC", score: 837, obligaciones: 17, vigentes: 8, aportantes: 1, cotizante: "Pensionado", nombre_vi: "Amparo Atehortua Osorio" },
    { nombre: "Mayra Alejandra Montoya Gomez", cedula: "1035439344", apellido: "MONTOYA", tipo: "CC", score: 744, obligaciones: 18, vigentes: 2, aportantes: 1, cotizante: "Empleado" },
    { nombre: "Reinaldo de Jesus Pulgarin Mejia", cedula: "71600926", apellido: "PULGARIN", tipo: "CC", score: 795, obligaciones: 26, vigentes: 7, aportantes: 2, cotizante: "Empleado / Pensionado" },
    { nombre: "Fabian David Arias Lopez", cedula: "1003045051", apellido: "ARIAS", tipo: "CC", score: 607, obligaciones: 24, vigentes: 8, aportantes: 2, cotizante: "Empleado" },
    { nombre: "Juan Diego Cardenas Toro", cedula: "1035066669", apellido: "CARDENAS", tipo: "CC", score: 342, obligaciones: 7, vigentes: 7, aportantes: 3, cotizante: "Empleado" },
    { nombre: "Maria Fernanda Carrasquilla Jaramillo", cedula: "1045423627", apellido: "CARRASQUILLA", tipo: "CC", score: 683, obligaciones: 18, vigentes: 10, aportantes: 2, cotizante: "Pensionado / Empleado" },
    { nombre: "Maria Fernanda Perez Torres", cedula: "1018234280", apellido: "PEREZ", tipo: "CC", score: 674, obligaciones: 9, vigentes: 7, aportantes: 1, cotizante: "Empleado" },
    { nombre: "Cristian Camilo Velasquez Ramirez", cedula: "1040739580", apellido: "VELASQUEZ", tipo: "CC", score: 653, obligaciones: 15, vigentes: 2, aportantes: 3, cotizante: "Empleado", nombre_vi: "Luz Elena de Jesus Velasquez Ramirez" },
    { nombre: "Adriana Maria Saenz Jurado", cedula: "39439164", apellido: "SAENZ", tipo: "CC", score: 735, obligaciones: 45, vigentes: 10, aportantes: 1, cotizante: "Pensionado" },
    { nombre: "Jorge Luis Arevalo Guerra", cedula: "77034739", apellido: "AREVALO", tipo: "CC", score: 704, obligaciones: 165, vigentes: 19, aportantes: 2, cotizante: "Empleado" },
    { nombre: "Guillermo Leon Montoya Gomez", cedula: "8434598", apellido: "MONTOYA", tipo: "CC", score: 502, obligaciones: 14, vigentes: 5, aportantes: 2, cotizante: "Empleado / Pensionado" },
    { nombre: "Pedro Yezid Buitrago Pulido", cedula: "79704267", apellido: "BUITRAGO", tipo: "CC", score: 763, obligaciones: 85, vigentes: 11, aportantes: 1, cotizante: "Empleado" },
    { nombre: "Claudia Maria Restrepo Vasquez", cedula: "43737805", apellido: "RESTREPO", tipo: "CC", score: 837, obligaciones: 39, vigentes: 7, aportantes: 1, cotizante: "Empleado" },
    { nombre: "Aura Cristina Lopez Bracamonte", cedula: "1003434832", apellido: "LOPEZ", tipo: "CC", score: 0, obligaciones: 63, vigentes: 5, aportantes: 2, cotizante: "Empleado" },
    { nombre: "Claudia Patricia Gomez Escobar", cedula: "43546366", apellido: "GOMEZ", tipo: "CC", score: 850, obligaciones: 47, vigentes: 6, aportantes: 2, cotizante: "Pensionado / Empleado" },
];

// ---------------------------------------------------------------------
// Referencias a clientes de cualquiera de las dos bases.
// Una referencia es un string "mock:<idx>" (Perfiles de Prueba) o
// "exp:<idx>" (Base Experian Demo). La selección se guarda como
// { principal, secundario, parentesco }: ver guardarSeleccionMuestra().
// ---------------------------------------------------------------------

const BASE_MOCK = 'mock';
const BASE_EXPERIAN = 'exp';

function capitalizar(txt) {
    return String(txt || '').toLowerCase().replace(/(^|\s)\S/g, function(c) { return c.toUpperCase(); });
}

// Devuelve un objeto normalizado con los datos que necesita la Solicitud,
// o null si la referencia no es válida.
function resolverSolicitante(ref) {
    if (ref === null || ref === undefined || ref === '') return null;
    var base, idx;
    if (typeof ref === 'number') {
        base = BASE_MOCK; idx = ref;                 // compatibilidad con selecciones antiguas
    } else {
        var partes = String(ref).split(':');
        if (partes.length === 1) { base = BASE_MOCK; idx = parseInt(partes[0]); }
        else { base = partes[0]; idx = parseInt(partes[1]); }
    }
    if (isNaN(idx)) return null;

    if (base === BASE_MOCK) {
        var s = SOLICITANTES[idx];
        if (!s) return null;
        var d = s.data.data;
        return {
            ref: BASE_MOCK + ':' + idx, base: BASE_MOCK, idx: idx,
            nombre: s.nombre,
            descripcion: s.descripcion,
            primer_nombre: d.primer_nombre_persona_natural,
            primer_apellido: d.primer_apellido_persona_natural,
            tipo_id: 'CC',
            numero_id: d.numero_identificacion_persona_natural,
            valor_ingreso: s.data,     // mock de Valor Ingreso
        };
    }
    if (base === BASE_EXPERIAN) {
        var e = EXPERIAN_DEMO[idx];
        if (!e) return null;
        return {
            ref: BASE_EXPERIAN + ':' + idx, base: BASE_EXPERIAN, idx: idx,
            nombre: e.nombre,
            descripcion: 'Experian UAT — Score ' + (e.score || 'N/A') + ', ' + e.obligaciones + ' obligaciones, ' + resumenValorIngreso(e),
            primer_nombre: e.nombre.split(' ')[0].toUpperCase(),
            primer_apellido: e.apellido,
            tipo_id: e.tipo,
            numero_id: e.cedula,
            score: e.score,
            valor_ingreso: null,       // se consulta en vivo: ver obtenerValorIngreso()
        };
    }
    return null;
}

// Texto corto del Valor Ingreso de un cliente de la Base Experian Demo.
function resumenValorIngreso(e) {
    return e.cotizante + ' (' + e.aportantes + (e.aportantes === 1 ? ' aportante' : ' aportantes') + ')';
}

// Devuelve el Valor Ingreso de un solicitante ya resuelto: el mock de los
// Perfiles de Prueba o, para la Base Experian Demo, la consulta en vivo a
// Experian UAT. Lanza Error si Experian no responde con información.
async function obtenerValorIngreso(sol) {
    if (!sol) return null;
    if (sol.valor_ingreso) return sol.valor_ingreso;
    if (sol.base !== BASE_EXPERIAN) return null;
    var resp = await fetch('/experian/valor-ingreso', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            numero_documento: sol.numero_id,
            primer_apellido: sol.primer_apellido,
            tipo_documento: sol.tipo_id,
        }),
    });
    if (!resp.ok) {
        var detalle = 'Error ' + resp.status;
        try { detalle = (await resp.json()).detail || detalle; } catch (e) {}
        throw new Error('Valor Ingreso de ' + sol.nombre + ' (' + sol.tipo_id + ' ' + sol.numero_id + '): ' + detalle);
    }
    return await resp.json();
}

// ---------------------------------------------------------------------
// La selección hecha en /muestra se guarda en localStorage para que la vean
// todas las pestañas (Muestra y Solicitud suelen estar abiertas a la vez).
// Solo contiene referencias ("exp:3"), no datos personales. Lo que se deriva
// de ella (carpeta, centrales, HDC) sigue en sessionStorage, por pestaña.
// ---------------------------------------------------------------------

const CLAVE_SELECCION = 'morada_seleccion';

// Texto JSON de la selección vigente, o null.
function leerSeleccionCruda() {
    try {
        return localStorage.getItem(CLAVE_SELECCION) || sessionStorage.getItem(CLAVE_SELECCION);
    } catch (e) {
        return null;
    }
}

// Una selección nueva invalida la carpeta y los datos de centrales anteriores
// de esta pestaña.
function invalidarDatosDeSeleccion() {
    sessionStorage.removeItem('morada_carpeta');
    sessionStorage.removeItem('morada_centrales');
    sessionStorage.removeItem('morada_hdc');
    sessionStorage.removeItem('morada_ingresos');     // resultado del Análisis de Ingresos
    sessionStorage.removeItem('morada_capacidad');    // último cálculo de Capacidad de Pago
}

// Guarda { principal, secundario, parentesco }. Devuelve true si cambió.
function guardarSeleccionMuestra(seleccion) {
    var raw = JSON.stringify(seleccion);
    if (leerSeleccionCruda() === raw) return false;
    localStorage.setItem(CLAVE_SELECCION, raw);
    sessionStorage.removeItem(CLAVE_SELECCION);      // copia del formato anterior
    invalidarDatosDeSeleccion();
    return true;
}

function borrarSeleccionMuestra() {
    if (leerSeleccionCruda() === null) return;
    localStorage.removeItem(CLAVE_SELECCION);
    sessionStorage.removeItem(CLAVE_SELECCION);
    invalidarDatosDeSeleccion();
}

// Lee la selección y devuelve { principal, secundario, parentesco } ya
// resueltos (o null si no hay selección). Acepta el formato antiguo
// { principalIdx, secundarioIdx }.
function leerSeleccionMuestra() {
    var raw = leerSeleccionCruda();
    if (!raw) return null;
    try {
        var sel = JSON.parse(raw);
        var refP = sel.principal !== undefined ? sel.principal : sel.principalIdx;
        var refS = sel.secundario !== undefined ? sel.secundario : sel.secundarioIdx;
        var principal = resolverSolicitante(refP);
        if (!principal) return null;
        return {
            principal: principal,
            secundario: (refS === null || refS === undefined) ? null : resolverSolicitante(refS),
            parentesco: sel.parentesco || null,
        };
    } catch (e) {
        return null;
    }
}

// Llena un <select> con las dos bases agrupadas.
function poblarSelectConBases(sel) {
    var gMock = document.createElement('optgroup');
    gMock.label = 'Perfiles de Prueba';
    SOLICITANTES.forEach(function(s, i) {
        var opt = document.createElement('option');
        opt.value = BASE_MOCK + ':' + i;
        opt.textContent = (i + 1) + '. ' + s.nombre + ' — ' + s.descripcion;
        gMock.appendChild(opt);
    });
    sel.appendChild(gMock);

    var gExp = document.createElement('optgroup');
    gExp.label = 'Base Experian Demo (Valor Ingreso y HDC+ UAT)';
    EXPERIAN_DEMO.forEach(function(e, i) {
        var opt = document.createElement('option');
        opt.value = BASE_EXPERIAN + ':' + i;
        opt.textContent = (i + 1) + '. ' + e.nombre + ' (' + e.tipo + ' ' + e.cedula + ') — Score ' + (e.score || 'N/A');
        gExp.appendChild(opt);
    });
    sel.appendChild(gExp);
}
