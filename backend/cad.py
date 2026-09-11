import math
import re


def _triangles_from_ascii_stl(text):
    nums = re.findall(r"vertex\s+([-+0-9.eE]+)\s+([-+0-9.eE]+)\s+([-+0-9.eE]+)", text)
    vertices = [(float(x), float(y), float(z)) for x, y, z in nums]
    return [vertices[i:i + 3] for i in range(0, len(vertices) - 2, 3)]


def _cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def _sub(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def _norm(v):
    return math.sqrt(sum(x * x for x in v))


def analyze_ascii_stl(text):
    triangles = _triangles_from_ascii_stl(text)
    if not triangles:
        raise ValueError("No ASCII STL vertices found")

    points = [p for tri in triangles for p in tri]
    mins = [min(p[i] for p in points) for i in range(3)]
    maxs = [max(p[i] for p in points) for i in range(3)]
    area = 0.0
    signed_volume = 0.0
    for a, b, c in triangles:
        area += 0.5 * _norm(_cross(_sub(b, a), _sub(c, a)))
        signed_volume += (a[0] * (b[1] * c[2] - b[2] * c[1]) - a[1] * (b[0] * c[2] - b[2] * c[0]) + a[2] * (b[0] * c[1] - b[1] * c[0])) / 6.0

    dims = [maxs[i] - mins[i] for i in range(3)]
    return {
        "format": "ASCII STL",
        "triangle_count": len(triangles),
        "bounding_box": {"x": dims[0], "y": dims[1], "z": dims[2]},
        "surface_area": area,
        "volume": abs(signed_volume),
        "units": "model units; STL has no unit metadata",
        "analysis_status": "ANALYTICAL_AID",
        "engineering_note": "Geometry measurements do not constitute BIS certification or a standards pass/fail decision."
    }
