import React from "react";
import { Card, CardContent } from "../../../../components/common/Card.jsx";
import { EmptyState } from "../../../../components/common/EmptyState.jsx";
import { sportIcons } from "../../../../utils/constants.jsx";
import { capitalizeFirstLetter } from "../../../../utils/formatters.js";

export function SportDistribution({chartData}) {
    const totalFields = chartData.reduce((acc, curr) => acc + curr.count, 0);

    return (
        <Card>
            <CardContent className="content">
                <h3>Fields by Sport</h3>
                <div className="sport-list">
                    {chartData.map((item) => {
                        const sportName = item.sport.toLowerCase();
                        return (
                            <div key={sportName} className="sport-item">
                                <div className="sport-row">
                                    <div className="sport-name">
                                        <span className="sport-icon">
                                            {sportIcons[sportName] || "🏟️"}
                                        </span>
                                        <span>
                                            {capitalizeFirstLetter(sportName)}
                                        </span>
                                    </div>

                                    <span className="sport-count">
                                        {item.count}
                                    </span>
                                </div>

                                <div className="progress">
                                    <div
                                        className={`progress-bar ${sportName}`}
                                        style={{width: `${totalFields ? (item.count / totalFields) * 100 : 0}%`}}
                                    />
                                </div>
                            </div>
                        )
                    })}

                    {chartData.length === 0 && (
                        <EmptyState text="fields" />
                    )}
                </div>
            </CardContent>
        </Card>
    );
}