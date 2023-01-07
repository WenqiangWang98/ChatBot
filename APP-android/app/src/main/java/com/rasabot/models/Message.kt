package com.rasabot.models

import com.rasabot.util.Constants

data class Message(
    var message: String?= null,
    var id: Int = Constants.USER,
    var imageUrl: String?=null
)
