package cn.edu.fudan.cs.dstree.dynamicsplit;

import java.io.Serializable;

/**
 * Created by IntelliJ IDEA.
 * User: wangyang
 * Date: 11-7-5
 * Time: 下午8:09
 * To change this template use File | Settings | File Templates.
 */
public interface IRange extends Serializable {
    double calc(Sketch sketch, int len);
}
