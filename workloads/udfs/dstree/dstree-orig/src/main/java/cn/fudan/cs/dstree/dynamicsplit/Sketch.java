package cn.edu.fudan.cs.dstree.dynamicsplit;

import java.io.Serializable;
import java.util.Arrays;

/**
 * Created by IntelliJ IDEA.
 * User: wangyang
 * Date: 11-7-7
 * Time: 下午8:13
 * To change this template use File | Settings | File Templates.
 */
public class Sketch implements Serializable {
    float[] indicators;    //todo:wy
    @Override
    public String toString() {
	return Arrays.toString(indicators);
    }
}
