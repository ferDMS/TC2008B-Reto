Shader "Custom/TVColorEffect"
{
    Properties
    {
        _MainTex ("Texture", 2D) = "white" {}
        _ScanlineIntensity ("Scanline Intensity", Range(0, 1)) = 0.5
        _Distortion ("Distortion", Range(0, 1)) = 0.2
        _ColorTint ("Color Tint", Color) = (1, 1, 1, 1)
    }
    SubShader
    {
        Tags { "RenderType"="Opaque" }
        Pass
        {
            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag
            #include "UnityCG.cginc"

            struct appdata_t
            {
                float4 vertex : POSITION;
                float2 uv : TEXCOORD0;
            };

            struct v2f
            {
                float4 pos : SV_POSITION;
                float2 uv : TEXCOORD0;
            };

            sampler2D _MainTex;
            float _ScanlineIntensity;
            float _Distortion;
            float4 _ColorTint;

            v2f vert (appdata_t v)
            {
                v2f o;
                o.pos = UnityObjectToClipPos(v.vertex);
                o.uv = v.uv;
                return o;
            }

            float4 frag (v2f i) : SV_Target
            {
                // Distorsión horizontal tipo TV antigua
                float2 uv = i.uv;
                uv.x += sin(uv.y * 50.0) * _Distortion;

                // Textura base
                float4 texColor = tex2D(_MainTex, uv);

                // Añade scanlines
                float scanline = sin(uv.y * 300.0) * 0.5 + 0.5;
                texColor.rgb *= lerp(1.0, scanline, _ScanlineIntensity);

                // Aplica un tinte de color
                texColor.rgb *= _ColorTint.rgb;

                return texColor;
            }
            ENDCG
        }
    }
}
