shader_type canvas_item;
// Use only the edited silhouette. The latest source artwork retains all RGB
// pixels, including the face, so cleanup cannot redesign the character.
uniform sampler2D clean_silhouette : filter_linear_mipmap;
void fragment() {
    COLOR.a *= smoothstep(0.12, 0.8, texture(clean_silhouette, UV).a);
}
