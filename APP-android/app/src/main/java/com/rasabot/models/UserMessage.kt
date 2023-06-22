package com.rasabot.models

import com.rasabot.util.Constants

data class UserMessage(
    var message: String?= null,
    var id: Int = Constants.USER
)
