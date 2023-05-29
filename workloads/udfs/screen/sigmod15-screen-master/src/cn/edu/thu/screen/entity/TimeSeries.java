package cn.edu.thu.screen.entity;

import java.util.ArrayList;

/**
 * Created by Stoke on 2017/10/7.
 * E-mail address is zaqthss2009@gmail.com
 * Copyright © Stoke. All Rights Reserved.
 *
 * @author Stoke
 */
public class TimeSeries {
  private ArrayList<TimePoint> timeseries;

  public TimeSeries(ArrayList<TimePoint> timeseries) {
    setTimeseries(timeseries);
  }

  public TimeSeries() {
    setTimeseries(new ArrayList<TimePoint>());
  }

  public ArrayList<TimePoint> getTimeseries() {
    return timeseries;
  }

  public void setTimeseries(ArrayList<TimePoint> timeseries) {
    this.timeseries = timeseries;
  }

  public int getLength() {
    return timeseries.size();
  }

  public void addTimePoint(TimePoint tp) {
    timeseries.add(tp);
  }
}
