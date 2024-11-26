Shader "Custom/AdvancedBlurShader"
{
    Properties
    {
        _MainTex ("Base (RGB)", 2D) = "white" {}
        _BlurSize ("Blur Size", Range(0.0, 20.0)) = 1.0
    }
    SubShader
    {
        Tags { "RenderType"="Opaque" }
        Pass
        {
            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag

            sampler2D _MainTex;
            float4 _MainTex_TexelSize;
            float _BlurSize;

            struct appdata_t
            {
                float4 vertex : POSITION;
                float2 uv : TEXCOORD0;
            };

            struct v2f
            {
                float2 uv : TEXCOORD0;
                float4 vertex : SV_POSITION;
            };

            v2f vert (appdata_t v)
            {
                v2f o;
                o.vertex = UnityObjectToClipPos(v.vertex);
                o.uv = v.uv;
                return o;
            }

            fixed4 frag (v2f i) : SV_Target
            {
                fixed4 color = 0;
                float2 uv = i.uv;

                // Incrementa el número de muestras para un desenfoque más intenso
                for (int x = -5; x <= 5; x++)
                {
                    for (int y = -5; y <= 5; y++)
                    {
                        float2 offset = float2(x, y) * _BlurSize * _MainTex_TexelSize.xy;
                        color += tex2D(_MainTex, uv + offset);
                    }
                }

                return color / 121; // Promedio de las muestras (11x11 = 121 muestras)
            }
            ENDCG
        }
    }
}
