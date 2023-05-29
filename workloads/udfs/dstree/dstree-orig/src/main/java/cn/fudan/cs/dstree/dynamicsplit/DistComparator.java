package cn.edu.fudan.cs.dstree.dynamicsplit;

import java.util.Comparator;

/**
 * Created by IntelliJ IDEA.
 * User: ZhuShengqi
 * Date: 11-7-19
 * Time: 下午6:30
 * To change this template use File | Settings | File Templates.
 */
public class DistComparator implements Comparator<PqItem> {
    public int compare(PqItem item_1, PqItem item_2) {
        if (item_1.dist < item_2.dist) {
            return -1;
        }
        if (item_1.dist > item_2.dist) {
            return 1;
        }
        return 0;
    }
}
