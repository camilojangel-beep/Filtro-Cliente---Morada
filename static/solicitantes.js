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

function poblarSelectSolicitantes() {
    for (const id of ['selectPrincipal', 'selectSecundario']) {
        const sel = document.getElementById(id);
        if (!sel) continue;
        SOLICITANTES.forEach((s, i) => {
            const opt = document.createElement('option');
            opt.value = i;
            opt.textContent = (i + 1) + '. ' + s.nombre + ' — ' + s.descripcion;
            sel.appendChild(opt);
        });
    }
}
