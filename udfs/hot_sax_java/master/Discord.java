package master;

public class Discord {
	public int position;
	public double distance;

	public Discord(double distance, int position) {
		this.position = position;
		this.distance = distance;
	}

	@Override
	public String toString() {
		return "Discord(dist=" + Double.toString(distance) + ", pos=" + Integer.toString(position) + ")";
	}
}
