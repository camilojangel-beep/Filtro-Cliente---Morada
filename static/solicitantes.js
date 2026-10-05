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

// Base Experian Demo (UAT): personas que responden los DOS informes, Valor
// Ingreso y HDC+. La lista trae datos personales (nombre, cédula, score), así
// que vive en static/experian_demo.local.js, que está en .gitignore y no se
// sube al repositorio. Las páginas cargan ese archivo antes que este; si no
// existe, la base queda vacía y la app sigue funcionando con los Perfiles de
// Prueba. Formato de cada registro: ver static/experian_demo.local.example.js.
const EXPERIAN_DEMO = window.EXPERIAN_DEMO_LOCAL || [];

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
