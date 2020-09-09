package com.example.myapplication;

import android.app.Application;

import org.xutils.x;

public class MainApplication extends Application {
    @Override
    public void onCreate() {
        super.onCreate();
        x.Ext.init(this);
        x.Ext.setDebug(true);//是否输出Debug日志
    }
}
